"""
Flower ClientApp using Message API for federated learning
Supports external HTTP API for triggering training
"""
import flwr as fl
from flwr.app import ArrayRecord, Context, Message, MetricRecord, RecordDict, ConfigRecord
from flwr.clientapp import ClientApp
import torch
import torch.nn as nn
import os
import sys
from pathlib import Path
from typing import Dict, Optional
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

# Import model from server directory
sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))

from model import InsuranceCostModel
from data_loader import DataLoaderClient


class ClientState:
    """Shared state for client"""
    def __init__(self, client_id: int, data_dir: str = "output"):
        self.client_id = client_id
        self.data_dir = data_dir
        
        # Initialize data loader
        self.data_loader = DataLoaderClient(client_id, data_dir)
        
        # Determine input size from data
        df = self.data_loader.load_data()
        features, _ = self.data_loader.preprocess_features(df)
        self.input_size = features.shape[1]
        
        # Initialize model
        self.model = InsuranceCostModel(input_size=self.input_size)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Loss and optimizer
        self.criterion = nn.MSELoss()
        self.learning_rate = float(os.getenv("LEARNING_RATE", "0.001"))
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # Data loaders
        self.batch_size = int(os.getenv("BATCH_SIZE", "32"))
        self.train_loader, self.val_loader = self.data_loader.get_data_loaders(
            batch_size=self.batch_size
        )
        
        print(f"Client {client_id}: Initialized")
        print(f"  Input features: {self.input_size}")
        print(f"  Train batches: {len(self.train_loader)}")
        print(f"  Val batches: {len(self.val_loader)}")
        
        # Training status
        self.training_status = {
            "is_training": False,
            "last_training_round": None,
            "last_loss": None,
            "last_eval_loss": None,
        }


# Global state instance
_client_state: Optional[ClientState] = None


def get_client_state() -> ClientState:
    """Get or create client state"""
    global _client_state
    if _client_state is None:
        client_id = int(os.getenv("CLIENT_ID", "1"))
        data_dir = os.getenv("DATA_DIR", "output")
        _client_state = ClientState(client_id, data_dir)
    return _client_state


# Create ClientApp
app = ClientApp()


@app.train()
def train(msg: Message, context: Context) -> Message:
    """Train the model on local data."""
    state = get_client_state()
    state.training_status["is_training"] = True
    
    try:
        # Read ArrayRecord received from ServerApp
        arrays = msg.content.get("arrays")
        if arrays is not None:
            # Load weights to model
            state.model.load_state_dict(arrays.to_torch_state_dict())
        
        # Read config if provided
        config = msg.content.get("config", ConfigRecord({}))
        local_epochs = int(config.get("local_epochs", os.getenv("LOCAL_EPOCHS", "5")))
        
        # Update learning rate if provided
        if "learning_rate" in config:
            learning_rate = float(config["learning_rate"])
            for param_group in state.optimizer.param_groups:
                param_group['lr'] = learning_rate
        
        # Train model
        state.model.train()
        total_loss = 0.0
        num_samples = 0
        
        for epoch in range(local_epochs):
            epoch_loss = 0.0
            epoch_samples = 0
            
            for features, targets in state.train_loader:
                features = features.to(state.device)
                targets = targets.to(state.device).unsqueeze(1)
                
                # Forward pass
                state.optimizer.zero_grad()
                outputs = state.model(features)
                loss = state.criterion(outputs, targets)
                
                # Backward pass
                loss.backward()
                state.optimizer.step()
                
                epoch_loss += loss.item()
                epoch_samples += len(features)
            
            total_loss += epoch_loss
            num_samples = epoch_samples
        
        # Calculate average loss
        avg_loss = total_loss / (local_epochs * len(state.train_loader))
        
        print(f"Client {state.client_id}: Training completed")
        print(f"  Average loss: {avg_loss:.4f}")
        print(f"  Samples: {num_samples}")
        
        # Update status
        state.training_status["last_training_round"] = config.get("server_round", None)
        state.training_status["last_loss"] = avg_loss
        state.training_status["is_training"] = False
        
        # Construct reply Message
        model_record = ArrayRecord(state.model.state_dict())
        metrics = MetricRecord({
            "train_loss": avg_loss,
            "num-examples": num_samples,
        })
        
        content = RecordDict({"arrays": model_record, "metrics": metrics})
        return Message(content=content, reply_to=msg)
        
    except Exception as e:
        state.training_status["is_training"] = False
        print(f"Error in training: {e}")
        import traceback
        traceback.print_exc()
        raise


@app.evaluate()
def evaluate(msg: Message, context: Context) -> Message:
    """Evaluate the model on local data."""
    state = get_client_state()
    
    try:
        # Read ArrayRecord received from ServerApp
        arrays = msg.content.get("arrays")
        if arrays is not None:
            # Load weights to model
            state.model.load_state_dict(arrays.to_torch_state_dict())
        
        # Evaluate model
        state.model.eval()
        total_loss = 0.0
        num_samples = 0
        
        with torch.no_grad():
            for features, targets in state.val_loader:
                features = features.to(state.device)
                targets = targets.to(state.device).unsqueeze(1)
                
                outputs = state.model(features)
                loss = state.criterion(outputs, targets)
                
                total_loss += loss.item()
                num_samples += len(features)
        
        avg_loss = total_loss / len(state.val_loader)
        mse = avg_loss
        rmse = mse ** 0.5
        
        print(f"Client {state.client_id}: Evaluation completed")
        print(f"  MSE: {mse:.4f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  Samples: {num_samples}")
        
        # Update status
        state.training_status["last_eval_loss"] = mse
        
        # Construct reply Message
        metrics = MetricRecord({
            "eval_loss": mse,
            "eval_rmse": rmse,
            "num-examples": num_samples,
        })
        
        content = RecordDict({"metrics": metrics})
        return Message(content=content, reply_to=msg)
        
    except Exception as e:
        print(f"Error in evaluation: {e}")
        import traceback
        traceback.print_exc()
        raise


# HTTP API for external requests
http_app = Flask(__name__)
CORS(http_app)  # Enable CORS for external requests


@http_app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    state = get_client_state()
    return jsonify({
        "status": "healthy",
        "client_id": state.client_id,
        "model_input_size": state.input_size,
        "training_status": state.training_status,
    })


@http_app.route("/status", methods=["GET"])
def status():
    """Get training status"""
    state = get_client_state()
    return jsonify({
        "client_id": state.client_id,
        "training_status": state.training_status,
        "model_info": {
            "input_size": state.input_size,
            "device": str(state.device),
            "train_batches": len(state.train_loader),
            "val_batches": len(state.val_loader),
        }
    })


@http_app.route("/train/trigger", methods=["POST"])
def trigger_training():
    """
    Trigger training request from external service
    Note: This endpoint acknowledges the request, but actual training
    happens when server initiates federated learning round.
    """
    state = get_client_state()
    
    if state.training_status["is_training"]:
        return jsonify({
            "status": "already_training",
            "message": "Training is already in progress"
        }), 409
    
    # Get training parameters from request
    data = request.get_json() or {}
    local_epochs = data.get("local_epochs", int(os.getenv("LOCAL_EPOCHS", "5")))
    learning_rate = data.get("learning_rate", float(os.getenv("LEARNING_RATE", "0.001")))
    batch_size = data.get("batch_size", int(os.getenv("BATCH_SIZE", "32")))
    
    # Update configuration
    if learning_rate != state.learning_rate:
        state.learning_rate = learning_rate
        for param_group in state.optimizer.param_groups:
            param_group['lr'] = learning_rate
    
    if batch_size != state.batch_size:
        state.batch_size = batch_size
        state.train_loader, state.val_loader = state.data_loader.get_data_loaders(
            batch_size=batch_size
        )
    
    return jsonify({
        "status": "request_received",
        "message": "Training request received. Training will start when server initiates federated learning round.",
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
    state = get_client_state()
    
    # Get model parameters count
    total_params = sum(p.numel() for p in state.model.parameters())
    trainable_params = sum(p.numel() for p in state.model.parameters() if p.requires_grad)
    
    return jsonify({
        "client_id": state.client_id,
        "model": {
            "input_size": state.input_size,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "device": str(state.device),
        },
        "data": {
            "train_samples": len(state.train_loader.dataset) if hasattr(state.train_loader, 'dataset') else None,
            "val_samples": len(state.val_loader.dataset) if hasattr(state.val_loader, 'dataset') else None,
            "train_batches": len(state.train_loader),
            "val_batches": len(state.val_loader),
        }
    })


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


def main():
    """Start Flower ClientApp with HTTP API"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flower ClientApp with HTTP API")
    parser.add_argument("--client-id", type=int, default=int(os.getenv("CLIENT_ID", "1")), 
                       help="Client ID")
    parser.add_argument("--server-address", type=str, 
                       default=os.getenv("FLOWER_SERVER_URL", "localhost:8080").replace("http://", ""),
                       help="Flower server address")
    parser.add_argument("--data-dir", type=str, default=os.getenv("DATA_DIR", "output"),
                       help="Directory containing CSV files")
    parser.add_argument("--http-port", type=int, default=int(os.getenv("HTTP_PORT", "8081")),
                       help="HTTP API port")
    parser.add_argument("--enable-http", action="store_true", default=True,
                       help="Enable HTTP API server")
    args = parser.parse_args()
    
    # Set environment for client state
    os.environ["CLIENT_ID"] = str(args.client_id)
    os.environ["DATA_DIR"] = args.data_dir
    
    # Initialize client state
    get_client_state()
    
    # Start HTTP API if enabled
    if args.enable_http:
        start_http_server(args.http_port)
    
    print(f"Starting Flower ClientApp {args.client_id}")
    print(f"Server address: {args.server_address}")
    print(f"Data directory: {args.data_dir}")
    
    # Start Flower client using ClientApp
    # For Flower 1.21+ with Message API, use start_clientapp
    # For older versions, this will need to be adapted
    try:
        # Try new Message API (Flower 1.21+)
        from flwr.clientapp import start_clientapp
        print("Using Flower Message API (ClientApp)")
        start_clientapp(
            server_address=args.server_address,
            app=app,
        )
    except (ImportError, AttributeError) as e:
        # Fallback: Use legacy NumPyClient API
        print(f"Warning: Message API not available ({e}).")
        print("Please upgrade Flower to version 1.21+ for Message API support.")
        print("For now, use flower_client/client.py for legacy API support.")
        print("\nTo use Message API, upgrade Flower:")
        print("  pip install --upgrade flwr>=1.21.0")
        sys.exit(1)


if __name__ == "__main__":
    main()

