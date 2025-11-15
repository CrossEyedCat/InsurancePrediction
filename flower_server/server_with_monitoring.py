"""
Flower server with monitoring and HTTP API
"""
import flwr as fl
from flwr.server.strategy import FedAvg
from flwr.server import ServerConfig
import torch
import os
from pathlib import Path
from datetime import datetime
import threading
from flask import Flask, jsonify
from flask_cors import CORS

from model import InsuranceCostModel, get_model_parameters, set_model_parameters
from server import SaveModelStrategy, fit_config, evaluate_config, get_initial_parameters
from monitoring import get_monitor

# Configuration
# Use localhost instead of 0.0.0.0 on Windows to avoid binding issues
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))
HTTP_PORT = int(os.getenv("HTTP_PORT", "8082"))
NUM_ROUNDS = int(os.getenv("NUM_ROUNDS", "10"))
MIN_CLIENTS = int(os.getenv("MIN_CLIENTS", "3"))
FRACTION_FIT = float(os.getenv("FRACTION_FIT", "1.0"))
FRACTION_EVALUATE = float(os.getenv("FRACTION_EVALUATE", "1.0"))
MIN_AVAILABLE_CLIENTS = int(os.getenv("MIN_AVAILABLE_CLIENTS", "3"))

MODEL_DIR = Path("./models")
MODEL_DIR.mkdir(exist_ok=True)

# HTTP API for monitoring
http_app = Flask(__name__)
CORS(http_app)


@http_app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "flower_server"})


@http_app.route("/monitoring/status", methods=["GET"])
def monitoring_status():
    """Get current training status"""
    monitor = get_monitor()
    return jsonify(monitor.get_current_status())


@http_app.route("/monitoring/history", methods=["GET"])
def monitoring_history():
    """Get training history"""
    monitor = get_monitor()
    limit = int(os.getenv("HISTORY_LIMIT", "10"))
    return jsonify({
        "history": monitor.get_round_history(limit),
        "total_rounds": monitor.total_rounds
    })


@http_app.route("/monitoring/round/<int:round_num>", methods=["GET"])
def round_details(round_num):
    """Get details of a specific round"""
    monitor = get_monitor()
    details = monitor.get_round_details(round_num)
    if details:
        return jsonify(details)
    return jsonify({"error": "Round not found"}), 404


@http_app.route("/monitoring/summary", methods=["GET"])
def monitoring_summary():
    """Get metrics summary"""
    monitor = get_monitor()
    return jsonify(monitor.get_metrics_summary())


def start_http_server(port: int = 8082):
    """Start HTTP API server in a separate thread"""
    def run_server():
        http_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    print(f"Monitoring HTTP API started on port {port}")
    print(f"  Status: http://localhost:{port}/monitoring/status")
    print(f"  History: http://localhost:{port}/monitoring/history")
    print(f"  Summary: http://localhost:{port}/monitoring/summary")


def main():
    """Start Flower server with monitoring"""
    print("Starting Flower server with monitoring...")
    print(f"Server address: {SERVER_ADDRESS}:{SERVER_PORT}")
    print(f"HTTP API port: {HTTP_PORT}")
    print(f"Configuration:")
    print(f"  - Rounds: {NUM_ROUNDS}")
    print(f"  - Min clients: {MIN_CLIENTS}")
    print(f"  - Fraction fit: {FRACTION_FIT}")
    
    # Start HTTP API
    start_http_server(HTTP_PORT)
    
    # Create strategy
    strategy = SaveModelStrategy(
        fraction_fit=FRACTION_FIT,
        fraction_evaluate=FRACTION_EVALUATE,
        min_fit_clients=MIN_CLIENTS,
        min_evaluate_clients=MIN_CLIENTS,
        min_available_clients=max(MIN_CLIENTS, MIN_AVAILABLE_CLIENTS),
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

