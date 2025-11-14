"""
Flower client for federated learning
"""
import flwr as fl
import torch
import torch.nn as nn
from typing import Dict, Tuple, Optional
import os
import sys
from pathlib import Path

# Import model from server directory
# In production, this should be a shared package
sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))

from model import InsuranceCostModel, get_model_parameters, set_model_parameters
from data_loader import DataLoaderClient


class FlowerClient(fl.client.NumPyClient):
    """Flower client for federated learning"""
    
    def __init__(
        self,
        institution_id: int,
        database_url: str,
        local_epochs: int = 5,
        batch_size: int = 32,
        learning_rate: float = 0.001
    ):
        self.institution_id = institution_id
        self.local_epochs = local_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        
        # Initialize data loader
        self.data_loader = DataLoaderClient(institution_id, database_url)
        
        # Initialize model
        self.model = InsuranceCostModel()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Loss and optimizer
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Data loaders
        self.train_loader = None
        self.val_loader = None
        self._load_data()
    
    def _load_data(self):
        """Load training and validation data"""
        try:
            self.train_loader, self.val_loader = self.data_loader.get_data_loaders(
                batch_size=self.batch_size
            )
            print(f"Institution {self.institution_id}: Loaded data successfully")
            print(f"  Train batches: {len(self.train_loader)}")
            print(f"  Val batches: {len(self.val_loader)}")
        except Exception as e:
            print(f"Error loading data for institution {self.institution_id}: {e}")
            raise
    
    def get_parameters(self, config: Dict):
        """Get model parameters"""
        return get_model_parameters(self.model)
    
    def set_parameters(self, parameters):
        """Set model parameters"""
        set_model_parameters(self.model, parameters)
    
    def fit(self, parameters, config: Dict):
        """Train model on local data"""
        # Set parameters from server
        self.set_parameters(parameters)
        
        # Update learning rate if provided
        if "learning_rate" in config:
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = config["learning_rate"]
        
        # Train model
        self.model.train()
        total_loss = 0.0
        num_samples = 0
        
        for epoch in range(self.local_epochs):
            epoch_loss = 0.0
            epoch_samples = 0
            
            for features, targets in self.train_loader:
                features = features.to(self.device)
                targets = targets.to(self.device).unsqueeze(1)
                
                # Forward pass
                self.optimizer.zero_grad()
                outputs = self.model(features)
                loss = self.criterion(outputs, targets)
                
                # Backward pass
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
                epoch_samples += len(features)
            
            total_loss += epoch_loss
            num_samples = epoch_samples
        
        # Get updated parameters
        updated_parameters = self.get_parameters(config)
        
        # Calculate average loss
        avg_loss = total_loss / (self.local_epochs * len(self.train_loader))
        
        print(f"Institution {self.institution_id}: Training completed")
        print(f"  Average loss: {avg_loss:.4f}")
        print(f"  Samples: {num_samples}")
        
        return updated_parameters, num_samples, {"loss": avg_loss}
    
    def evaluate(self, parameters, config: Dict):
        """Evaluate model on local validation data"""
        # Set parameters from server
        self.set_parameters(parameters)
        
        # Evaluate model
        self.model.eval()
        total_loss = 0.0
        num_samples = 0
        
        with torch.no_grad():
            for features, targets in self.val_loader:
                features = features.to(self.device)
                targets = targets.to(self.device).unsqueeze(1)
                
                outputs = self.model(features)
                loss = self.criterion(outputs, targets)
                
                total_loss += loss.item()
                num_samples += len(features)
        
        avg_loss = total_loss / len(self.val_loader)
        mse = avg_loss
        
        print(f"Institution {self.institution_id}: Evaluation completed")
        print(f"  MSE: {mse:.4f}")
        print(f"  Samples: {num_samples}")
        
        return float(avg_loss), num_samples, {"mse": mse}


def main():
    """Start Flower client"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flower Client")
    parser.add_argument("--institution-id", type=int, required=True, help="Institution ID")
    parser.add_argument("--server-address", type=str, default=os.getenv("FLOWER_SERVER_URL", "localhost:8080").replace("http://", ""), help="Flower server address")
    args = parser.parse_args()
    
    institution_id = args.institution_id
    server_address = args.server_address
    
    # Get configuration from environment
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://medical_user:medical_pass@localhost:5432/medical_insurance"
    )
    local_epochs = int(os.getenv("LOCAL_EPOCHS", "5"))
    batch_size = int(os.getenv("BATCH_SIZE", "32"))
    learning_rate = float(os.getenv("LEARNING_RATE", "0.001"))
    
    print(f"Starting Flower client for institution {institution_id}")
    print(f"Server address: {server_address}")
    print(f"Configuration:")
    print(f"  - Local epochs: {local_epochs}")
    print(f"  - Batch size: {batch_size}")
    print(f"  - Learning rate: {learning_rate}")
    
    # Create client
    client = FlowerClient(
        institution_id=institution_id,
        database_url=database_url,
        local_epochs=local_epochs,
        batch_size=batch_size,
        learning_rate=learning_rate
    )
    
    # Start client
    fl.client.start_numpy_client(
        server_address=server_address,
        client=client
    )


if __name__ == "__main__":
    main()

