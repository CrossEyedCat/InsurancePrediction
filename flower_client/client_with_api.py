"""
Flower client with HTTP API for external requests
Uses NumPyClient API for compatibility, adds HTTP API layer
"""
import flwr as fl
import torch
import torch.nn as nn
from typing import Dict
import os
import sys
from pathlib import Path
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

# Import monitoring FIRST from current directory (client) to avoid conflicts
# Use absolute path and unique module name to prevent conflicts with server monitoring
_client_dir = Path(__file__).parent.absolute()
_monitoring_file = _client_dir / "monitoring.py"

# Import monitoring module directly from file using absolute path
import importlib.util
monitoring_spec = importlib.util.spec_from_file_location(
    "flower_client_monitoring",  # Unique name to avoid conflicts
    str(_monitoring_file)
)
client_monitoring = importlib.util.module_from_spec(monitoring_spec)
monitoring_spec.loader.exec_module(client_monitoring)
get_monitor = client_monitoring.get_monitor

# Verify the function signature
import inspect
sig = inspect.signature(get_monitor)
if len(sig.parameters) != 1:
    raise ImportError(f"get_monitor from client monitoring has wrong signature: {sig}")

# Now import model from server directory
server_path = str(Path(__file__).parent.parent / "flower_server")
sys.path.insert(0, server_path)

from model import InsuranceCostModel, get_model_parameters, set_model_parameters
from data_loader import DataLoaderClient


class FlowerClientWithAPI(fl.client.NumPyClient):
    """Flower client with HTTP API support"""
    
    def __init__(
        self,
        client_id: int,
        data_dir: str = "output",
        local_epochs: int = 5,
        batch_size: int = 32,
        learning_rate: float = 0.001
    ):
        self.client_id = client_id
        self.local_epochs = local_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        
        # Initialize data loader
        self.data_loader = DataLoaderClient(client_id, data_dir)
        
        # Determine input size from data
        self._determine_input_size()
        
        # Initialize model
        self.model = InsuranceCostModel(input_size=self.input_size)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Loss and optimizer
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Data loaders
        self.train_loader = None
        self.val_loader = None
        self._load_data()
        
        # Training status
        self.training_status = {
            "is_training": False,
            "last_training_round": None,
            "last_loss": None,
            "last_eval_loss": None,
        }
    
    def _determine_input_size(self):
        """Determine input size from data"""
        df = self.data_loader.load_data()
        features, _ = self.data_loader.preprocess_features(df)
        self.input_size = features.shape[1]
    
    def _load_data(self):
        """Load training and validation data"""
        try:
            self.train_loader, self.val_loader = self.data_loader.get_data_loaders(
                batch_size=self.batch_size
            )
            print(f"Client {self.client_id}: Loaded data successfully")
            print(f"  Train batches: {len(self.train_loader)}")
            print(f"  Val batches: {len(self.val_loader)}")
            print(f"  Input features: {self.input_size}")
        except Exception as e:
            print(f"Error loading data for client {self.client_id}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_parameters(self, config: Dict):
        """Get model parameters"""
        return get_model_parameters(self.model)
    
    def set_parameters(self, parameters):
        """Set model parameters"""
        set_model_parameters(self.model, parameters)
    
    def fit(self, parameters, config: Dict):
        """Train model on local data"""
        from datetime import datetime
        import time
        
        self.training_status["is_training"] = True
        monitor = get_monitor(self.client_id)
        round_num = config.get("server_round", 0)
        start_time = time.time()
        
        try:
            # Record training start
            monitor.start_training(round_num, config)
            
            # Set parameters from server
            self.set_parameters(parameters)
            
            # Update learning rate if provided
            if "learning_rate" in config:
                for param_group in self.optimizer.param_groups:
                    param_group['lr'] = config["learning_rate"]
            
            # Update local epochs if provided
            local_epochs = int(config.get("local_epochs", self.local_epochs))
            
            # Train model
            self.model.train()
            total_loss = 0.0
            num_samples = 0
            
            for epoch in range(local_epochs):
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
            avg_loss = total_loss / (local_epochs * len(self.train_loader))
            duration = time.time() - start_time
            
            print(f"Client {self.client_id}: Training completed")
            print(f"  Average loss: {avg_loss:.4f}")
            print(f"  Samples: {num_samples}")
            print(f"  Duration: {duration:.2f}s")
            
            # Record metrics
            monitor.record_training_metrics(round_num, avg_loss, num_samples, local_epochs, duration)
            
            # Update status
            self.training_status["last_training_round"] = round_num
            self.training_status["last_loss"] = avg_loss
            self.training_status["is_training"] = False
            
            return updated_parameters, num_samples, {"loss": avg_loss, "client_id": self.client_id}
            
        except Exception as e:
            self.training_status["is_training"] = False
            print(f"Error in training: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def evaluate(self, parameters, config: Dict):
        """Evaluate model on local validation data"""
        import time
        
        monitor = get_monitor(self.client_id)
        round_num = config.get("server_round", 0)
        start_time = time.time()
        
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
        duration = time.time() - start_time
        
        print(f"Client {self.client_id}: Evaluation completed")
        print(f"  MSE: {mse:.4f}")
        print(f"  RMSE: {mse**0.5:.2f}")
        print(f"  Samples: {num_samples}")
        print(f"  Duration: {duration:.2f}s")
        
        # Record metrics
        monitor.record_evaluation_metrics(round_num, avg_loss, mse, num_samples, duration)
        
        # Update status
        self.training_status["last_eval_loss"] = mse
        
        return float(avg_loss), num_samples, {"mse": mse, "client_id": self.client_id}


# Global client instance for HTTP API
_client_instance: FlowerClientWithAPI = None


def get_client_instance() -> FlowerClientWithAPI:
    """Get global client instance"""
    global _client_instance
    return _client_instance


# HTTP API
http_app = Flask(__name__)
CORS(http_app)


@http_app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    client = get_client_instance()
    if client is None:
        return jsonify({"status": "not_initialized"}), 503
    
    return jsonify({
        "status": "healthy",
        "client_id": client.client_id,
        "model_input_size": client.input_size,
        "training_status": client.training_status,
    })


@http_app.route("/status", methods=["GET"])
def status():
    """Get training status"""
    client = get_client_instance()
    if client is None:
        return jsonify({"error": "Client not initialized"}), 503
    
    return jsonify({
        "client_id": client.client_id,
        "training_status": client.training_status,
        "model_info": {
            "input_size": client.input_size,
            "device": str(client.device),
            "train_batches": len(client.train_loader),
            "val_batches": len(client.val_loader),
        }
    })


@http_app.route("/train/trigger", methods=["POST"])
def trigger_training():
    """Trigger training request from external service"""
    client = get_client_instance()
    if client is None:
        return jsonify({"error": "Client not initialized"}), 503
    
    if client.training_status["is_training"]:
        return jsonify({
            "status": "already_training",
            "message": "Training is already in progress"
        }), 409
    
    # Get training parameters from request
    data = request.get_json() or {}
    local_epochs = data.get("local_epochs", client.local_epochs)
    learning_rate = data.get("learning_rate", client.learning_rate)
    batch_size = data.get("batch_size", client.batch_size)
    
    # Update configuration
    if learning_rate != client.learning_rate:
        client.learning_rate = learning_rate
        for param_group in client.optimizer.param_groups:
            param_group['lr'] = learning_rate
    
    if batch_size != client.batch_size:
        client.batch_size = batch_size
        client.local_epochs = local_epochs
        client.train_loader, client.val_loader = client.data_loader.get_data_loaders(
            batch_size=batch_size
        )
    else:
        client.local_epochs = local_epochs
    
    return jsonify({
        "status": "request_received",
        "message": "Training configuration updated. Training will start when server initiates federated learning round.",
        "configuration": {
            "local_epochs": local_epochs,
            "learning_rate": learning_rate,
            "batch_size": batch_size,
        },
        "note": "Actual training happens when Flower server starts a federated learning round. This endpoint only updates configuration."
    })


@http_app.route("/model/info", methods=["GET"])
def model_info():
    """Get model information"""
    client = get_client_instance()
    if client is None:
        return jsonify({"error": "Client not initialized"}), 503
    
    total_params = sum(p.numel() for p in client.model.parameters())
    trainable_params = sum(p.numel() for p in client.model.parameters() if p.requires_grad)
    
    return jsonify({
        "client_id": client.client_id,
        "model": {
            "input_size": client.input_size,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "device": str(client.device),
        },
        "data": {
            "train_samples": len(client.train_loader.dataset) if hasattr(client.train_loader, 'dataset') else None,
            "val_samples": len(client.val_loader.dataset) if hasattr(client.val_loader, 'dataset') else None,
            "train_batches": len(client.train_loader),
            "val_batches": len(client.val_loader),
        }
    })


@http_app.route("/monitoring/status", methods=["GET"])
def monitoring_status():
    """Get monitoring status"""
    client = get_client_instance()
    if client is None:
        return jsonify({"error": "Client not initialized"}), 503
    
    # Use the imported get_monitor function
    monitor = get_monitor(client.client_id)
    return jsonify(monitor.get_current_status())


@http_app.route("/monitoring/history", methods=["GET"])
def monitoring_history():
    """Get training history"""
    client = get_client_instance()
    if client is None:
        return jsonify({"error": "Client not initialized"}), 503
    
    monitor = get_monitor(client.client_id)
    limit = int(request.args.get("limit", 20))
    return jsonify({
        "history": monitor.get_training_history(limit),
        "client_id": client.client_id
    })


@http_app.route("/monitoring/summary", methods=["GET"])
def monitoring_summary():
    """Get metrics summary"""
    client = get_client_instance()
    if client is None:
        return jsonify({"error": "Client not initialized"}), 503
    
    monitor = get_monitor(client.client_id)
    return jsonify(monitor.get_metrics_summary())


def start_http_server(port: int = 8081):
    """Start HTTP API server in a separate thread"""
    def run_server():
        http_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    print(f"HTTP API server started on port {port}")
    print(f"  Health check: http://localhost:{port}/health")
    print(f"  Status: http://localhost:{port}/status")
    print(f"  Trigger training: POST http://localhost:{port}/train/trigger")
    print(f"  Model info: http://localhost:{port}/model/info")
    print(f"  Monitoring status: http://localhost:{port}/monitoring/status")
    print(f"  Monitoring history: http://localhost:{port}/monitoring/history")
    print(f"  Monitoring summary: http://localhost:{port}/monitoring/summary")


def main():
    """Start Flower client with HTTP API"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flower Client with HTTP API")
    parser.add_argument("--client-id", type=int, required=True, help="Client ID (1, 2, or 3)")
    parser.add_argument("--server-address", type=str, 
                       default=os.getenv("FLOWER_SERVER_URL", "localhost:8080").replace("http://", ""),
                       help="Flower server address")
    parser.add_argument("--data-dir", type=str, default="output", help="Directory containing CSV files")
    parser.add_argument("--http-port", type=int, default=int(os.getenv("HTTP_PORT", "8081")),
                       help="HTTP API port")
    parser.add_argument("--enable-http", action="store_true", default=True,
                       help="Enable HTTP API server")
    args = parser.parse_args()
    
    # Get configuration from environment
    local_epochs = int(os.getenv("LOCAL_EPOCHS", "5"))
    batch_size = int(os.getenv("BATCH_SIZE", "32"))
    learning_rate = float(os.getenv("LEARNING_RATE", "0.001"))
    
    # Create client
    global _client_instance
    _client_instance = FlowerClientWithAPI(
        client_id=args.client_id,
        data_dir=args.data_dir,
        local_epochs=local_epochs,
        batch_size=batch_size,
        learning_rate=learning_rate
    )
    
    print(f"Starting Flower client {args.client_id}")
    print(f"Server address: {args.server_address}")
    print(f"Data directory: {args.data_dir}")
    print(f"Configuration:")
    print(f"  - Local epochs: {local_epochs}")
    print(f"  - Batch size: {batch_size}")
    print(f"  - Learning rate: {learning_rate}")
    
    # Start HTTP API if enabled
    if args.enable_http:
        start_http_server(args.http_port)
    
    # Start Flower client
    print(f"Connecting to server at {args.server_address}...")
    fl.client.start_numpy_client(
        server_address=args.server_address,
        client=_client_instance
    )


if __name__ == "__main__":
    main()

