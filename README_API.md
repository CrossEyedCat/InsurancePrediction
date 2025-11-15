# Flower Federated Learning API - Quick Start

## Overview

The Flower federated learning system provides HTTP REST APIs for monitoring and interacting with the training process. This guide provides a quick introduction to using these APIs.

## Quick Start

### 1. Start the System

```bash
# Windows
scripts\start_full_training.bat

# Or manually:
# Terminal 1: Server
python flower_server\server_with_monitoring.py

# Terminal 2-4: Clients
python flower_client\client_with_api.py --client-id 1 --http-port 8081
python flower_client\client_with_api.py --client-id 2 --http-port 8083
python flower_client\client_with_api.py --client-id 3 --http-port 8084
```

### 2. Test the APIs

```bash
# Quick test
python scripts\quick_monitoring_test.py

# Full test
python scripts\test_monitoring.py
```

### 3. Access APIs

**Server Monitoring:**
- Status: http://localhost:8082/monitoring/status
- History: http://localhost:8082/monitoring/history
- Summary: http://localhost:8082/monitoring/summary

**Client Monitoring (Client 1):**
- Status: http://localhost:8081/monitoring/status
- History: http://localhost:8081/monitoring/history
- Summary: http://localhost:8081/monitoring/summary

## API Endpoints Summary

### Server (Port 8082)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/monitoring/status` | GET | Current training status |
| `/monitoring/history` | GET | Training history |
| `/monitoring/round/<N>` | GET | Round details |
| `/monitoring/summary` | GET | Metrics summary |

### Client (Ports 8081, 8083, 8084)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | Client status |
| `/train/trigger` | POST | Update training config |
| `/model/info` | GET | Model information |
| `/monitoring/status` | GET | Monitoring status |
| `/monitoring/history` | GET | Training history |
| `/monitoring/summary` | GET | Metrics summary |

## Quick Examples

### Python

```python
import requests

# Server status
status = requests.get("http://localhost:8082/monitoring/status").json()
print(f"Round: {status['current_round']}, Training: {status['is_training']}")

# Client status
client_status = requests.get("http://localhost:8081/monitoring/status").json()
print(f"Client trainings: {client_status['total_trainings']}")

# Update training config
requests.post("http://localhost:8081/train/trigger", json={
    "local_epochs": 5,
    "learning_rate": 0.001
})
```

### cURL

```bash
# Server status
curl http://localhost:8082/monitoring/status

# Client status
curl http://localhost:8081/monitoring/status

# Update config
curl -X POST http://localhost:8081/train/trigger \
  -H "Content-Type: application/json" \
  -d '{"local_epochs": 5, "learning_rate": 0.001}'
```

## Documentation

- **Full API Documentation**: `API_DOCUMENTATION.md`
- **Quick Reference**: `API_QUICK_REFERENCE.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **Usage Examples**: `API_EXAMPLES.md`

## Response Format

All APIs return JSON responses:

**Success (200):**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

**Error (4xx/5xx):**
```json
{
  "error": "Error message"
}
```

## Common Use Cases

1. **Monitor Training Progress**: Use `/monitoring/status` to check current round
2. **Get Training History**: Use `/monitoring/history` to see past rounds
3. **Update Configuration**: Use `/train/trigger` to change training parameters
4. **Compare Performance**: Use `/monitoring/summary` to get statistics
5. **Export Metrics**: Fetch history and save to file for analysis

## Next Steps

1. Read `API_DOCUMENTATION.md` for complete API reference
2. Check `API_EXAMPLES.md` for code examples
3. Use `TESTING_GUIDE.md` for testing procedures
4. See `TROUBLESHOOTING.md` for common issues

