# API Quick Reference

## Server API (Port 8082)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/monitoring/status` | GET | Current training status |
| `/monitoring/history` | GET | Training history |
| `/monitoring/round/<N>` | GET | Round details |
| `/monitoring/summary` | GET | Metrics summary |

## Client API (Ports 8081, 8083, 8084)

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

### Check Server Status
```bash
curl http://localhost:8082/monitoring/status
```

### Check Client Status
```bash
curl http://localhost:8081/monitoring/status
```

### Get Training History
```bash
curl http://localhost:8082/monitoring/history?limit=10
```

### Update Training Config
```bash
curl -X POST http://localhost:8081/train/trigger \
  -H "Content-Type: application/json" \
  -d '{"local_epochs": 5, "learning_rate": 0.001}'
```

### Get Metrics Summary
```bash
curl http://localhost:8082/monitoring/summary
curl http://localhost:8081/monitoring/summary
```

## Python Examples

```python
import requests

# Server status
server_status = requests.get("http://localhost:8082/monitoring/status").json()

# Client status
client_status = requests.get("http://localhost:8081/monitoring/status").json()

# Update config
requests.post("http://localhost:8081/train/trigger", json={
    "local_epochs": 5,
    "learning_rate": 0.001
})

# Get history
history = requests.get("http://localhost:8082/monitoring/history").json()
```

## Response Codes

- `200`: Success
- `404`: Not found
- `409`: Conflict (e.g., training in progress)
- `503`: Service unavailable

