"""
Flower server for federated aggregation
"""
import flwr as fl
from flwr.server.strategy import FedAvg
from flwr.server import ServerConfig
import torch
import os
from pathlib import Path
from datetime import datetime
from model import InsuranceCostModel, get_model_parameters, set_model_parameters
from monitoring import get_monitor

# Configuration
# Use localhost instead of 0.0.0.0 on Windows to avoid binding issues
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))
NUM_ROUNDS = int(os.getenv("NUM_ROUNDS", "10"))
MIN_CLIENTS = int(os.getenv("MIN_CLIENTS", "3"))  # Need 3 clients
FRACTION_FIT = float(os.getenv("FRACTION_FIT", "1.0"))  # Use all clients
FRACTION_EVALUATE = float(os.getenv("FRACTION_EVALUATE", "1.0"))  # Use all clients
MIN_AVAILABLE_CLIENTS = int(os.getenv("MIN_AVAILABLE_CLIENTS", "3"))  # Wait for 3 clients

MODEL_DIR = Path("./models")
MODEL_DIR.mkdir(exist_ok=True)


def get_initial_parameters():
    """Get initial model parameters"""
    # Use 17 features: 13 base + 4 regions
    model = InsuranceCostModel(input_size=17)
    return get_model_parameters(model)


def fit_config(server_round: int):
    """Return training configuration for each round"""
    config = {
        "server_round": server_round,
        "local_epochs": int(os.getenv("LOCAL_EPOCHS", "5")),
        "batch_size": int(os.getenv("BATCH_SIZE", "32")),
        "learning_rate": float(os.getenv("LEARNING_RATE", "0.001")),
    }
    return config


def evaluate_config(server_round: int):
    """Return evaluation configuration"""
    return {"server_round": server_round}


class SaveModelStrategy(FedAvg):
    """Custom strategy that saves model after aggregation"""
    
    def configure_fit(self, server_round, parameters, client_manager):
        """Configure fit for clients"""
        monitor = get_monitor()
        num_clients = len(client_manager.all().values())
        monitor.start_round(server_round, num_clients)
        return super().configure_fit(server_round, parameters, client_manager)
    
    def aggregate_fit(self, server_round, results, failures):
        """Aggregate model weights and save model"""
        monitor = get_monitor()
        
        # Record client metrics
        for result in results:
            if result[1].metrics:
                client_id = result[1].metrics.get("client_id", 0)
                num_samples = result[1].num_examples
                metrics = result[1].metrics
                monitor.record_fit_metrics(server_round, client_id, metrics, num_samples)
        
        # Call parent aggregation
        aggregated_parameters, aggregated_metrics = super().aggregate_fit(
            server_round, results, failures
        )
        
        if aggregated_parameters is not None:
            # Save aggregated model
            # Determine input size (17 features: 13 base + 4 regions)
            model = InsuranceCostModel(input_size=17)
            set_model_parameters(model, aggregated_parameters)
            
            # Save model checkpoint
            model_path = MODEL_DIR / f"model_round_{server_round}.pt"
            torch.save(model.state_dict(), model_path)
            
            # Save as active model
            active_model_path = MODEL_DIR / "active_model.pt"
            torch.save(model.state_dict(), active_model_path)
            
            print(f"Model saved: {model_path}")
            print(f"Active model updated: {active_model_path}")
        
        # Record completion
        monitor.complete_round(server_round, aggregated_metrics)
        
        return aggregated_parameters, aggregated_metrics
    
    def aggregate_evaluate(self, server_round, results, failures):
        """Aggregate evaluation results"""
        monitor = get_monitor()
        
        # Record client evaluation metrics
        for result in results:
            if result[1].metrics:
                client_id = result[1].metrics.get("client_id", 0)
                num_samples = result[1].num_examples
                metrics = result[1].metrics
                monitor.record_eval_metrics(server_round, client_id, metrics, num_samples)
        
        return super().aggregate_evaluate(server_round, results, failures)


def main():
    """Start Flower server"""
    print("Starting Flower server...")
    print(f"Server address: {SERVER_ADDRESS}:{SERVER_PORT}")
    print(f"Configuration:")
    print(f"  - Rounds: {NUM_ROUNDS}")
    print(f"  - Min clients: {MIN_CLIENTS}")
    print(f"  - Fraction fit: {FRACTION_FIT}")
    
    # Create strategy
    strategy = SaveModelStrategy(
        fraction_fit=FRACTION_FIT,
        fraction_evaluate=FRACTION_EVALUATE,
        min_fit_clients=MIN_CLIENTS,
        min_evaluate_clients=MIN_CLIENTS,
        min_available_clients=max(MIN_CLIENTS, MIN_AVAILABLE_CLIENTS),  # Ensure >= min_fit_clients
        initial_parameters=fl.common.ndarrays_to_parameters(get_initial_parameters()),
        on_fit_config_fn=fit_config,
        on_evaluate_config_fn=evaluate_config,
    )
    
    # Create server config
    config = ServerConfig(num_rounds=NUM_ROUNDS)
    
    # Start server
    fl.server.start_server(
        server_address=f"{SERVER_ADDRESS}:{SERVER_PORT}",
        config=config,
        strategy=strategy,
    )


if __name__ == "__main__":
    main()

