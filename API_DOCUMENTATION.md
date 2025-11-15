# Flower Federated Learning API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Server API](#server-api)
3. [Client API](#client-api)
4. [Testing Guide](#testing-guide)
5. [Examples](#examples)
6. [Error Handling](#error-handling)

## Overview

This documentation describes the HTTP API endpoints for monitoring and interacting with the Flower federated learning system. The system consists of:

- **Flower Server**: Aggregates model weights from clients (port 8080, monitoring API: 8082)
- **Flower Clients**: Train models locally on partitioned data (monitoring APIs: 8081, 8083, 8084)

All APIs return JSON responses and support CORS for browser-based requests.

## Server API

Base URL: `http://localhost:8082`

### Endpoints

#### 1. Health Check

**GET** `/health`

Check if the server is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "flower_server"
}
```

**Status Codes:**
- `200`: Server is healthy

---

#### 2. Get Training Status

**GET** `/monitoring/status`

Get current training status and server information.

**Response:**
```json
{
  "current_round": 5,
  "round_start_time": "2024-01-15T10:30:00.123456",
  "total_rounds": 5,
  "total_clients": 3,
  "uptime_seconds": 3600.5,
  "is_training": true
}
```

**Fields:**
- `current_round` (int|null): Current training round number, null if not training
- `round_start_time` (string|null): ISO timestamp when current round started
- `total_rounds` (int): Total number of rounds completed
- `total_clients` (int): Maximum number of clients that have participated
- `uptime_seconds` (float): Server uptime in seconds
- `is_training` (bool): Whether training is currently in progress

**Status Codes:**
- `200`: Success

---

#### 3. Get Training History

**GET** `/monitoring/history`

Get history of completed training rounds.

**Query Parameters:**
- `limit` (optional, int): Maximum number of rounds to return (default: 10)

**Response:**
```json
{
  "history": [
    {
      "round": 5,
      "started_at": "2024-01-15T10:30:00.123456",
      "completed_at": "2024-01-15T10:35:00.654321",
      "duration_seconds": 300.53,
      "status": "completed",
      "num_clients": 3,
      "aggregated_metrics": {
        "loss": 0.023456
      },
      "client_metrics": [
        {
          "round": 5,
          "client_id": 1,
          "num_samples": 13333,
          "metrics": {
            "loss": 0.0234,
            "client_id": 1
          },
          "timestamp": "2024-01-15T10:32:00.123456"
        }
      ]
    }
  ],
  "total_rounds": 5
}
```

**Fields:**
- `history` (array): List of training round records
  - `round` (int): Round number
  - `started_at` (string): ISO timestamp when round started
  - `completed_at` (string): ISO timestamp when round completed
  - `duration_seconds` (float): Round duration in seconds
  - `status` (string): Round status ("completed" or "in_progress")
  - `num_clients` (int): Number of clients that participated
  - `aggregated_metrics` (object): Aggregated metrics from all clients
  - `client_metrics` (array): Individual client metrics

**Status Codes:**
- `200`: Success

**Example:**
```bash
curl http://localhost:8082/monitoring/history?limit=5
```

---

#### 4. Get Round Details

**GET** `/monitoring/round/<round_num>`

Get detailed information about a specific training round.

**Path Parameters:**
- `round_num` (int): Round number

**Response:**
```json
{
  "round": 5,
  "started_at": "2024-01-15T10:30:00.123456",
  "completed_at": "2024-01-15T10:35:00.654321",
  "duration_seconds": 300.53,
  "status": "completed",
  "num_clients": 3,
  "aggregated_metrics": {
    "loss": 0.023456
  },
  "client_metrics": [
    {
      "round": 5,
      "client_id": 1,
      "num_samples": 13333,
      "metrics": {
        "loss": 0.0234,
        "client_id": 1
      },
      "timestamp": "2024-01-15T10:32:00.123456"
    },
    {
      "round": 5,
      "client_id": 2,
      "num_samples": 13333,
      "metrics": {
        "loss": 0.0245,
        "client_id": 2
      },
      "timestamp": "2024-01-15T10:32:05.123456"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `404`: Round not found

**Example:**
```bash
curl http://localhost:8082/monitoring/round/5
```

---

#### 5. Get Metrics Summary

**GET** `/monitoring/summary`

Get summary statistics of all training rounds.

**Response:**
```json
{
  "total_rounds": 5,
  "average_loss": 0.025000,
  "min_loss": 0.020000,
  "max_loss": 0.030000,
  "latest_round": 5,
  "latest_loss": 0.023456
}
```

**Fields:**
- `total_rounds` (int): Number of completed rounds
- `average_loss` (float|null): Average loss across all rounds
- `min_loss` (float|null): Minimum loss achieved
- `max_loss` (float|null): Maximum loss recorded
- `latest_round` (int|null): Most recent round number
- `latest_loss` (float|null): Loss from most recent round

**Status Codes:**
- `200`: Success

**Example:**
```bash
curl http://localhost:8082/monitoring/summary
```

---

## Client API

Base URLs:
- Client 1: `http://localhost:8081`
- Client 2: `http://localhost:8083`
- Client 3: `http://localhost:8084`

### Endpoints

#### 1. Health Check

**GET** `/health`

Check if the client is running and initialized.

**Response:**
```json
{
  "status": "healthy",
  "client_id": 1,
  "model_input_size": 17,
  "training_status": {
    "is_training": false,
    "last_training_round": 5,
    "last_loss": 0.0234,
    "last_eval_loss": 0.0256
  }
}
```

**Fields:**
- `status` (string): Health status
- `client_id` (int): Client identifier
- `model_input_size` (int): Number of input features
- `training_status` (object): Current training status
  - `is_training` (bool): Whether training is in progress
  - `last_training_round` (int|null): Last completed round number
  - `last_loss` (float|null): Loss from last training
  - `last_eval_loss` (float|null): Evaluation loss from last evaluation

**Status Codes:**
- `200`: Client is healthy
- `503`: Client not initialized

---

#### 2. Get Client Status

**GET** `/status`

Get detailed client status and configuration.

**Response:**
```json
{
  "client_id": 1,
  "training_status": {
    "is_training": false,
    "last_training_round": 5,
    "last_loss": 0.0234,
    "last_eval_loss": 0.0256
  },
  "model_info": {
    "input_size": 17,
    "device": "cpu",
    "train_batches": 417,
    "val_batches": 105
  }
}
```

**Status Codes:**
- `200`: Success
- `503`: Client not initialized

---

#### 3. Trigger Training Configuration Update

**POST** `/train/trigger`

Update training configuration. Note: Actual training starts when the Flower server initiates a federated learning round.

**Request Body:**
```json
{
  "local_epochs": 5,
  "learning_rate": 0.001,
  "batch_size": 32
}
```

**Request Fields:**
- `local_epochs` (optional, int): Number of local training epochs (default: current value)
- `learning_rate` (optional, float): Learning rate (default: current value)
- `batch_size` (optional, int): Batch size (default: current value)

**Response:**
```json
{
  "status": "request_received",
  "message": "Training configuration updated. Training will start when server initiates federated learning round.",
  "configuration": {
    "local_epochs": 5,
    "learning_rate": 0.001,
    "batch_size": 32
  },
  "note": "Actual training happens when Flower server starts a federated learning round. This endpoint only updates configuration."
}
```

**Status Codes:**
- `200`: Configuration updated successfully
- `409`: Training is already in progress
- `503`: Client not initialized

**Example:**
```bash
curl -X POST http://localhost:8081/train/trigger \
  -H "Content-Type: application/json" \
  -d '{"local_epochs": 5, "learning_rate": 0.001, "batch_size": 32}'
```

---

#### 4. Get Model Information

**GET** `/model/info`

Get information about the client's model and data.

**Response:**
```json
{
  "client_id": 1,
  "model": {
    "input_size": 17,
    "total_parameters": 48769,
    "trainable_parameters": 48769,
    "device": "cpu"
  },
  "data": {
    "train_samples": 13333,
    "val_samples": 3333,
    "train_batches": 417,
    "val_batches": 105
  }
}
```

**Fields:**
- `model` (object): Model information
  - `input_size` (int): Number of input features
  - `total_parameters` (int): Total number of model parameters
  - `trainable_parameters` (int): Number of trainable parameters
  - `device` (string): Device used ("cpu" or "cuda")
- `data` (object): Dataset information
  - `train_samples` (int|null): Number of training samples
  - `val_samples` (int|null): Number of validation samples
  - `train_batches` (int): Number of training batches
  - `val_batches` (int): Number of validation batches

**Status Codes:**
- `200`: Success
- `503`: Client not initialized

---

#### 5. Get Monitoring Status

**GET** `/monitoring/status`

Get current monitoring status of the client.

**Response:**
```json
{
  "client_id": 1,
  "current_training": {
    "round": 5,
    "started_at": "2024-01-15T10:30:00.123456",
    "config": {
      "server_round": 5,
      "local_epochs": 3,
      "batch_size": 32,
      "learning_rate": 0.001
    },
    "status": "training"
  },
  "total_trainings": 5,
  "total_evaluations": 5,
  "uptime_seconds": 3600.5,
  "is_training": true
}
```

**Fields:**
- `current_training` (object|null): Current training session information
  - `round` (int): Current round number
  - `started_at` (string): ISO timestamp when training started
  - `config` (object): Training configuration
  - `status` (string): Training status
- `total_trainings` (int): Total number of training sessions
- `total_evaluations` (int): Total number of evaluation sessions
- `uptime_seconds` (float): Client uptime in seconds
- `is_training` (bool): Whether training is currently in progress

**Status Codes:**
- `200`: Success
- `503`: Client not initialized

---

#### 6. Get Training History

**GET** `/monitoring/history`

Get history of training and evaluation sessions.

**Query Parameters:**
- `limit` (optional, int): Maximum number of records to return (default: 20)

**Response:**
```json
{
  "history": [
    {
      "round": 5,
      "type": "training",
      "loss": 0.0234,
      "num_samples": 13333,
      "local_epochs": 3,
      "duration_seconds": 45.2,
      "timestamp": "2024-01-15T10:30:45.123456"
    },
    {
      "round": 5,
      "type": "evaluation",
      "loss": 0.0256,
      "mse": 0.0256,
      "rmse": 0.16,
      "num_samples": 3333,
      "duration_seconds": 5.1,
      "timestamp": "2024-01-15T10:35:50.123456"
    }
  ],
  "client_id": 1
}
```

**Fields:**
- `history` (array): List of training/evaluation records
  - `round` (int): Round number
  - `type` (string): Record type ("training" or "evaluation")
  - `loss` (float): Loss value
  - `num_samples` (int): Number of samples processed
  - `local_epochs` (int, training only): Number of local epochs
  - `duration_seconds` (float): Duration in seconds
  - `timestamp` (string): ISO timestamp
  - `mse` (float, evaluation only): Mean Squared Error
  - `rmse` (float, evaluation only): Root Mean Squared Error

**Status Codes:**
- `200`: Success
- `503`: Client not initialized

**Example:**
```bash
curl "http://localhost:8081/monitoring/history?limit=10"
```

---

#### 7. Get Metrics Summary

**GET** `/monitoring/summary`

Get summary statistics of client training metrics.

**Response:**
```json
{
  "total_trainings": 5,
  "total_evaluations": 5,
  "average_training_loss": 0.025000,
  "average_eval_loss": 0.026000,
  "min_training_loss": 0.020000,
  "min_eval_loss": 0.021000,
  "latest_training_loss": 0.023400,
  "latest_eval_loss": 0.025600
}
```

**Fields:**
- `total_trainings` (int): Number of training sessions
- `total_evaluations` (int): Number of evaluation sessions
- `average_training_loss` (float|null): Average training loss
- `average_eval_loss` (float|null): Average evaluation loss
- `min_training_loss` (float|null): Minimum training loss
- `min_eval_loss` (float|null): Minimum evaluation loss
- `latest_training_loss` (float|null): Most recent training loss
- `latest_eval_loss` (float|null): Most recent evaluation loss

**Status Codes:**
- `200`: Success
- `503`: Client not initialized

---

## Testing Guide

### Prerequisites

1. Ensure all dependencies are installed:
   ```bash
   pip install flask flask-cors requests
   ```

2. Start the server:
   ```bash
   python flower_server/server_with_monitoring.py
   ```

3. Start clients:
   ```bash
   python flower_client/client_with_api.py --client-id 1 --http-port 8081
   python flower_client/client_with_api.py --client-id 2 --http-port 8083
   python flower_client/client_with_api.py --client-id 3 --http-port 8084
   ```

### Automated Testing

#### Quick Test Script

Run the quick monitoring test:
```bash
python scripts/quick_monitoring_test.py
```

This tests:
- Server health and monitoring endpoints
- Client health and monitoring endpoints
- Basic connectivity

#### Full Test Script

Run comprehensive API tests:
```bash
python scripts/test_monitoring.py
```

#### Client API Test

Test client-specific endpoints:
```bash
python scripts/test_client_api.py http://localhost:8081
```

### Manual Testing

#### Using cURL

**Server Status:**
```bash
curl http://localhost:8082/monitoring/status
```

**Server History:**
```bash
curl http://localhost:8082/monitoring/history?limit=5
```

**Client Status:**
```bash
curl http://localhost:8081/monitoring/status
```

**Trigger Training Config:**
```bash
curl -X POST http://localhost:8081/train/trigger \
  -H "Content-Type: application/json" \
  -d '{"local_epochs": 5, "learning_rate": 0.001}'
```

#### Using Python

```python
import requests

# Server status
response = requests.get("http://localhost:8082/monitoring/status")
print(response.json())

# Client status
response = requests.get("http://localhost:8081/monitoring/status")
print(response.json())

# Update training config
response = requests.post(
    "http://localhost:8081/train/trigger",
    json={"local_epochs": 5, "learning_rate": 0.001}
)
print(response.json())
```

#### Using JavaScript/Node.js

```javascript
const axios = require('axios');

// Server status
axios.get('http://localhost:8082/monitoring/status')
  .then(response => console.log(response.data));

// Client status
axios.get('http://localhost:8081/monitoring/status')
  .then(response => console.log(response.data));

// Trigger training
axios.post('http://localhost:8081/train/trigger', {
  local_epochs: 5,
  learning_rate: 0.001,
  batch_size: 32
})
  .then(response => console.log(response.data));
```

---

## Examples

### Example 1: Monitor Training Progress

```python
import requests
import time

def monitor_training(server_url, interval=5):
    """Monitor training progress"""
    while True:
        try:
            # Get server status
            status = requests.get(f"{server_url}/monitoring/status").json()
            
            if status.get("is_training"):
                round_num = status.get("current_round")
                print(f"Round {round_num} in progress...")
                
                # Get round details
                round_details = requests.get(
                    f"{server_url}/monitoring/round/{round_num}"
                ).json()
                
                if "aggregated_metrics" in round_details:
                    loss = round_details["aggregated_metrics"].get("loss")
                    print(f"  Current loss: {loss:.6f}")
            else:
                print("No training in progress")
            
            time.sleep(interval)
        except KeyboardInterrupt:
            break

# Monitor server
monitor_training("http://localhost:8082")
```

### Example 2: Get Training Statistics

```python
import requests

def get_training_stats(server_url, client_urls):
    """Get comprehensive training statistics"""
    stats = {}
    
    # Server summary
    server_summary = requests.get(f"{server_url}/monitoring/summary").json()
    stats["server"] = server_summary
    
    # Client summaries
    stats["clients"] = []
    for i, url in enumerate(client_urls, 1):
        try:
            client_summary = requests.get(f"{url}/monitoring/summary").json()
            stats["clients"].append({
                "client_id": i,
                "summary": client_summary
            })
        except Exception as e:
            print(f"Error getting client {i} stats: {e}")
    
    return stats

# Get stats
stats = get_training_stats(
    "http://localhost:8082",
    ["http://localhost:8081", "http://localhost:8083", "http://localhost:8084"]
)
print(stats)
```

### Example 3: Export Training History

```python
import requests
import json
from datetime import datetime

def export_training_history(server_url, output_file="training_history.json"):
    """Export complete training history"""
    # Get all rounds (use large limit)
    response = requests.get(f"{server_url}/monitoring/history?limit=1000")
    history = response.json()
    
    # Add export metadata
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "total_rounds": history.get("total_rounds", 0),
        "history": history.get("history", [])
    }
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"Exported {len(export_data['history'])} rounds to {output_file}")

# Export history
export_training_history("http://localhost:8082")
```

### Example 4: Real-time Dashboard

```python
import requests
import time
from datetime import datetime

def dashboard(server_url, client_urls, refresh_interval=2):
    """Simple text-based dashboard"""
    while True:
        try:
            # Clear screen (Unix/Linux/Mac)
            # For Windows, use: os.system('cls')
            print("\033[2J\033[H")  # ANSI escape codes
            
            print("=" * 70)
            print("Flower Federated Learning Dashboard")
            print("=" * 70)
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Server status
            server_status = requests.get(f"{server_url}/monitoring/status").json()
            print("SERVER STATUS:")
            print(f"  Current Round: {server_status.get('current_round', 'N/A')}")
            print(f"  Total Rounds: {server_status.get('total_rounds', 0)}")
            print(f"  Is Training: {server_status.get('is_training', False)}")
            print(f"  Uptime: {server_status.get('uptime_seconds', 0):.1f}s\n")
            
            # Server summary
            server_summary = requests.get(f"{server_url}/monitoring/summary").json()
            if "latest_loss" in server_summary:
                print("SERVER METRICS:")
                print(f"  Latest Loss: {server_summary.get('latest_loss', 'N/A'):.6f}")
                print(f"  Average Loss: {server_summary.get('average_loss', 'N/A'):.6f}")
                print(f"  Min Loss: {server_summary.get('min_loss', 'N/A'):.6f}\n")
            
            # Client statuses
            print("CLIENT STATUSES:")
            for i, url in enumerate(client_urls, 1):
                try:
                    client_status = requests.get(f"{url}/monitoring/status").json()
                    print(f"  Client {i}:")
                    print(f"    Trainings: {client_status.get('total_trainings', 0)}")
                    print(f"    Is Training: {client_status.get('is_training', False)}")
                    
                    client_summary = requests.get(f"{url}/monitoring/summary").json()
                    if "latest_training_loss" in client_summary:
                        print(f"    Latest Loss: {client_summary.get('latest_training_loss', 'N/A'):.6f}")
                except:
                    print(f"  Client {i}: Not available")
            
            print("\n" + "=" * 70)
            print("Press Ctrl+C to exit")
            
            time.sleep(refresh_interval)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(refresh_interval)

# Run dashboard
dashboard(
    "http://localhost:8082",
    ["http://localhost:8081", "http://localhost:8083", "http://localhost:8084"]
)
```

---

## Error Handling

### Common Error Responses

#### 503 Service Unavailable

**Server:**
```json
{
  "error": "Service not available"
}
```

**Client:**
```json
{
  "error": "Client not initialized"
}
```

**Causes:**
- Server/client not started
- Initialization not complete
- Data not loaded

**Solution:**
- Wait for initialization to complete
- Check server/client logs
- Ensure data files are available

#### 404 Not Found

```json
{
  "error": "Round not found"
}
```

**Causes:**
- Requested round doesn't exist
- Round number out of range

**Solution:**
- Check available rounds using `/monitoring/history`
- Use valid round numbers

#### 409 Conflict

```json
{
  "status": "already_training",
  "message": "Training is already in progress"
}
```

**Causes:**
- Attempting to update training config while training is active

**Solution:**
- Wait for current training to complete
- Check training status before updating config

### Error Response Format

All errors follow this format:
```json
{
  "error": "Error message description"
}
```

Additional fields may be included depending on the error type.

---

## Rate Limiting

Currently, there are no rate limits on API endpoints. However, for production deployments, consider:

- Implementing rate limiting for monitoring endpoints
- Using connection pooling for frequent requests
- Caching responses for static data

---

## Security Considerations

### Current Implementation

- APIs run on localhost by default
- No authentication required
- CORS enabled for browser access

### Production Recommendations

1. **Authentication**: Implement API keys or OAuth2
2. **HTTPS**: Use TLS/SSL for all connections
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Validate all request parameters
5. **Access Control**: Restrict access to authorized users only

---

## Troubleshooting

### API Not Responding

1. Check if server/client is running
2. Verify port is not occupied: `python scripts/check_ports.py`
3. Check firewall settings
4. Review server/client logs

### Incorrect Data

1. Verify data files exist in `output/` directory
2. Check data format matches expected schema
3. Review preprocessing logs

### Connection Errors

1. Ensure server is started before clients
2. Verify server address is correct (use `127.0.0.1` on Windows)
3. Check network connectivity

For more troubleshooting information, see `TROUBLESHOOTING.md`.

---

## Additional Resources

- **Monitoring Guide**: `MONITORING_GUIDE.md`
- **Client API Guide**: `CLIENT_API_GUIDE.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **Flower Documentation**: https://flower.ai/docs/

---

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Review server/client logs
3. Verify API endpoints are accessible
4. Check Flower framework documentation

