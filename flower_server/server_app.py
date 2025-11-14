"""
Flower server app using new API
This creates a server app that can be used with flower-superlink
"""
import flwr as fl
from flwr.server.strategy import FedAvg
from flwr.server import ServerConfig
import torch
import os
from pathlib import Path
from model import InsuranceCostModel, get_model_parameters, set_model_parameters

# Configuration
NUM_ROUNDS = int(os.getenv("NUM_ROUNDS", "10"))
MIN_CLIENTS = int(os.getenv("MIN_CLIENTS", "3"))
FRACTION_FIT = float(os.getenv("FRACTION_FIT", "1.0"))
FRACTION_EVALUATE = float(os.getenv("FRACTION_EVALUATE", "1.0"))
MIN_AVAILABLE_CLIENTS = int(os.getenv("MIN_AVAILABLE_CLIENTS", "3"))

MODEL_DIR = Path("./models")
MODEL_DIR.mkdir(exist_ok=True)


def get_initial_parameters():
    """Get initial model parameters"""
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
    
    def aggregate_fit(self, server_round, results, failures):
        """Aggregate model weights and save model"""
        aggregated_parameters, aggregated_metrics = super().aggregate_fit(
            server_round, results, failures
        )
        
        if aggregated_parameters is not None:
            model = InsuranceCostModel(input_size=17)
            set_model_parameters(model, aggregated_parameters)
            
            model_path = MODEL_DIR / f"model_round_{server_round}.pt"
            torch.save(model.state_dict(), model_path)
            
            active_model_path = MODEL_DIR / "active_model.pt"
            torch.save(model.state_dict(), active_model_path)
            
            print(f"Model saved: {model_path}")
            print(f"Active model updated: {active_model_path}")
        
        return aggregated_parameters, aggregated_metrics


# Create strategy
strategy = SaveModelStrategy(
    fraction_fit=FRACTION_FIT,
    fraction_evaluate=FRACTION_EVALUATE,
    min_fit_clients=MIN_CLIENTS,
    min_evaluate_clients=MIN_CLIENTS,
    min_available_clients=MIN_AVAILABLE_CLIENTS,
    initial_parameters=fl.common.ndarrays_to_parameters(get_initial_parameters()),
    on_fit_config_fn=fit_config,
    on_evaluate_config_fn=evaluate_config,
)

# Create server config
config = ServerConfig(num_rounds=NUM_ROUNDS)

# Create server app
app = fl.server.ServerApp(
    config=config,
    strategy=strategy,
)

if __name__ == "__main__":
    # For direct execution, use the old API (still works)
    print("Starting Flower server (using legacy API for compatibility)...")
    print(f"Configuration:")
    print(f"  - Rounds: {NUM_ROUNDS}")
    print(f"  - Min clients: {MIN_CLIENTS}")
    print(f"  - Fraction fit: {FRACTION_FIT}")
    
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=config,
        strategy=strategy,
    )

