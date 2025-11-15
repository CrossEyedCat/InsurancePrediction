# Testing Guide

## Overview

This guide provides comprehensive instructions for testing the Flower federated learning system, including server, clients, and monitoring APIs.

## Prerequisites

1. **Install Dependencies**
   ```bash
   pip install flask flask-cors requests
   ```

2. **Prepare Data**
   - Ensure CSV files are in `output/` directory
   - Verify data files: `patients.csv`, `lifestyle.csv`, etc.

3. **Check Ports**
   ```bash
   python scripts/check_ports.py
   ```

## Starting the System

### Option 1: Automated Start (Windows)

```bash
scripts\start_full_training.bat
```

This starts:
- Server on port 8080 (monitoring: 8082)
- Client 1 on port 8081
- Client 2 on port 8083
- Client 3 on port 8084

### Option 2: Manual Start

**Terminal 1 - Server:**
```bash
python flower_server\server_with_monitoring.py
```

**Terminal 2 - Client 1:**
```bash
python flower_client\client_with_api.py --client-id 1 --http-port 8081
```

**Terminal 3 - Client 2:**
```bash
python flower_client\client_with_api.py --client-id 2 --http-port 8083
```

**Terminal 4 - Client 3:**
```bash
python flower_client\client_with_api.py --client-id 3 --http-port 8084
```

## Testing Scripts

### 1. Quick Monitoring Test

**Purpose**: Basic connectivity and endpoint testing

**Usage:**
```bash
python scripts/quick_monitoring_test.py
```

**Tests:**
- Server health check
- Server monitoring endpoints
- Client health checks
- Client monitoring endpoints

**Expected Output:**
```
Testing Server Monitoring API (http://localhost:8082)...
  [OK] Status retrieved
  [OK] History retrieved
  [OK] Summary retrieved

Testing Client Monitoring API (http://localhost:8081)...
  [OK] Status retrieved
  [OK] History retrieved
  [OK] Summary retrieved
```

### 2. Full Monitoring Test

**Purpose**: Comprehensive API testing

**Usage:**
```bash
python scripts/test_monitoring.py
```

**Options:**
```bash
# Test only server
python scripts/test_monitoring.py --server-only

# Test only clients
python scripts/test_monitoring.py --client-only

# Custom URLs
python scripts/test_monitoring.py \
  --server-url http://localhost:8082 \
  --client-url http://localhost:8081
```

### 3. Client API Test

**Purpose**: Test client-specific endpoints

**Usage:**
```bash
python scripts/test_client_api.py http://localhost:8081
```

**Tests:**
- Health endpoint
- Status endpoint
- Model info endpoint
- Training trigger endpoint

## Manual Testing

### Server Endpoints

#### Health Check
```bash
curl http://localhost:8082/health
```

**Expected:**
```json
{"status": "healthy", "service": "flower_server"}
```

#### Get Status
```bash
curl http://localhost:8082/monitoring/status
```

**Expected:**
```json
{
  "current_round": 5,
  "total_rounds": 5,
  "is_training": true,
  ...
}
```

#### Get History
```bash
curl http://localhost:8082/monitoring/history?limit=5
```

#### Get Round Details
```bash
curl http://localhost:8082/monitoring/round/5
```

#### Get Summary
```bash
curl http://localhost:8082/monitoring/summary
```

### Client Endpoints

#### Health Check
```bash
curl http://localhost:8081/health
```

#### Get Status
```bash
curl http://localhost:8081/status
```

#### Trigger Training Config
```bash
curl -X POST http://localhost:8081/train/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "local_epochs": 5,
    "learning_rate": 0.001,
    "batch_size": 32
  }'
```

#### Get Model Info
```bash
curl http://localhost:8081/model/info
```

#### Get Monitoring Status
```bash
curl http://localhost:8081/monitoring/status
```

#### Get Monitoring History
```bash
curl "http://localhost:8081/monitoring/history?limit=10"
```

#### Get Monitoring Summary
```bash
curl http://localhost:8081/monitoring/summary
```

## Python Testing

### Basic Test Script

```python
import requests
import json

def test_server_api(base_url="http://localhost:8082"):
    """Test server API endpoints"""
    print("Testing Server API...")
    
    # Health check
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    print("✓ Health check passed")
    
    # Status
    response = requests.get(f"{base_url}/monitoring/status")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Status: Round {data.get('current_round')}")
    
    # History
    response = requests.get(f"{base_url}/monitoring/history")
    assert response.status_code == 200
    print("✓ History retrieved")
    
    # Summary
    response = requests.get(f"{base_url}/monitoring/summary")
    assert response.status_code == 200
    print("✓ Summary retrieved")

def test_client_api(base_url="http://localhost:8081"):
    """Test client API endpoints"""
    print("\nTesting Client API...")
    
    # Health check
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    print("✓ Health check passed")
    
    # Status
    response = requests.get(f"{base_url}/status")
    assert response.status_code == 200
    print("✓ Status retrieved")
    
    # Model info
    response = requests.get(f"{base_url}/model/info")
    assert response.status_code == 200
    print("✓ Model info retrieved")
    
    # Monitoring status
    response = requests.get(f"{base_url}/monitoring/status")
    assert response.status_code == 200
    print("✓ Monitoring status retrieved")

if __name__ == "__main__":
    test_server_api()
    test_client_api()
    print("\nAll tests passed!")
```

### Advanced Testing

```python
import requests
import time
from datetime import datetime

class FlowerAPITester:
    """Comprehensive API tester"""
    
    def __init__(self, server_url, client_urls):
        self.server_url = server_url
        self.client_urls = client_urls
    
    def test_connectivity(self):
        """Test basic connectivity"""
        print("Testing connectivity...")
        
        # Server
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            assert response.status_code == 200
            print("✓ Server is reachable")
        except Exception as e:
            print(f"✗ Server not reachable: {e}")
            return False
        
        # Clients
        for i, url in enumerate(self.client_urls, 1):
            try:
                response = requests.get(f"{url}/health", timeout=5)
                assert response.status_code == 200
                print(f"✓ Client {i} is reachable")
            except Exception as e:
                print(f"✗ Client {i} not reachable: {e}")
        
        return True
    
    def test_monitoring_during_training(self, duration=60):
        """Test monitoring during active training"""
        print(f"\nMonitoring training for {duration} seconds...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                # Server status
                status = requests.get(
                    f"{self.server_url}/monitoring/status"
                ).json()
                
                if status.get("is_training"):
                    round_num = status.get("current_round")
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Round {round_num} in progress")
                    
                    # Check clients
                    for i, url in enumerate(self.client_urls, 1):
                        client_status = requests.get(
                            f"{url}/monitoring/status"
                        ).json()
                        if client_status.get("is_training"):
                            print(f"  Client {i}: Training")
                
                time.sleep(5)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)
    
    def test_data_consistency(self):
        """Test data consistency across endpoints"""
        print("\nTesting data consistency...")
        
        # Get server summary
        server_summary = requests.get(
            f"{self.server_url}/monitoring/summary"
        ).json()
        
        # Get client summaries
        client_summaries = []
        for url in self.client_urls:
            try:
                summary = requests.get(f"{url}/monitoring/summary").json()
                client_summaries.append(summary)
            except:
                pass
        
        # Verify consistency
        if server_summary.get("total_rounds") > 0:
            print(f"✓ Server has {server_summary['total_rounds']} rounds")
        
        for i, summary in enumerate(client_summaries, 1):
            if summary.get("total_trainings", 0) > 0:
                print(f"✓ Client {i} has {summary['total_trainings']} trainings")
        
        return True

# Usage
tester = FlowerAPITester(
    "http://localhost:8082",
    ["http://localhost:8081", "http://localhost:8083", "http://localhost:8084"]
)

tester.test_connectivity()
tester.test_data_consistency()
```

## Integration Testing

### Test Full Training Cycle

```python
import requests
import time

def test_full_training_cycle():
    """Test complete training cycle"""
    
    server_url = "http://localhost:8082"
    client_urls = [
        "http://localhost:8081",
        "http://localhost:8083",
        "http://localhost:8084"
    ]
    
    print("Starting full training cycle test...")
    
    # 1. Check initial status
    print("\n1. Initial Status:")
    status = requests.get(f"{server_url}/monitoring/status").json()
    print(f"   Current round: {status.get('current_round')}")
    print(f"   Total rounds: {status.get('total_rounds')}")
    
    # 2. Update client configs
    print("\n2. Updating client configurations...")
    for url in client_urls:
        response = requests.post(
            f"{url}/train/trigger",
            json={"local_epochs": 3, "learning_rate": 0.001}
        )
        if response.status_code == 200:
            print(f"   ✓ {url}: Config updated")
    
    # 3. Monitor training
    print("\n3. Monitoring training...")
    max_wait = 300  # 5 minutes
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        status = requests.get(f"{server_url}/monitoring/status").json()
        
        if status.get("is_training"):
            round_num = status.get("current_round")
            print(f"   Round {round_num} in progress...")
            
            # Get round details
            round_details = requests.get(
                f"{server_url}/monitoring/round/{round_num}"
            ).json()
            
            if "aggregated_metrics" in round_details:
                loss = round_details["aggregated_metrics"].get("loss")
                print(f"   Loss: {loss:.6f}")
        else:
            print("   Training completed or not started")
            break
        
        time.sleep(10)
    
    # 4. Get final summary
    print("\n4. Final Summary:")
    summary = requests.get(f"{server_url}/monitoring/summary").json()
    print(f"   Total rounds: {summary.get('total_rounds')}")
    print(f"   Latest loss: {summary.get('latest_loss')}")
    
    print("\n✓ Full training cycle test completed")

test_full_training_cycle()
```

## Performance Testing

### Load Test

```python
import requests
import time
from concurrent.futures import ThreadPoolExecutor

def load_test_endpoint(url, endpoint, num_requests=100):
    """Load test an endpoint"""
    def make_request():
        try:
            response = requests.get(f"{url}{endpoint}", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(
            lambda _: make_request(),
            range(num_requests)
        ))
    
    duration = time.time() - start_time
    success_rate = sum(results) / len(results) * 100
    
    print(f"Endpoint: {endpoint}")
    print(f"  Requests: {num_requests}")
    print(f"  Duration: {duration:.2f}s")
    print(f"  Success rate: {success_rate:.1f}%")
    print(f"  Requests/sec: {num_requests/duration:.2f}")

# Test server endpoints
load_test_endpoint("http://localhost:8082", "/monitoring/status", 100)
load_test_endpoint("http://localhost:8082", "/monitoring/history", 100)
```

## Validation Tests

### Validate Response Formats

```python
import requests
import json

def validate_response_format(url, endpoint, expected_fields):
    """Validate response has expected fields"""
    response = requests.get(f"{url}{endpoint}")
    
    if response.status_code != 200:
        print(f"✗ {endpoint}: Status {response.status_code}")
        return False
    
    data = response.json()
    
    for field in expected_fields:
        if field not in data:
            print(f"✗ {endpoint}: Missing field '{field}'")
            return False
    
    print(f"✓ {endpoint}: Valid format")
    return True

# Validate server endpoints
validate_response_format(
    "http://localhost:8082",
    "/monitoring/status",
    ["current_round", "total_rounds", "is_training"]
)

validate_response_format(
    "http://localhost:8082",
    "/monitoring/summary",
    ["total_rounds"]
)

# Validate client endpoints
validate_response_format(
    "http://localhost:8081",
    "/monitoring/status",
    ["client_id", "total_trainings", "is_training"]
)
```

## Troubleshooting Tests

### Common Issues

1. **Port Already in Use**
   ```bash
   python scripts/check_ports.py
   scripts\stop_all_flower.bat
   ```

2. **Connection Refused**
   - Verify server/client is running
   - Check firewall settings
   - Verify correct port numbers

3. **503 Service Unavailable**
   - Wait for initialization
   - Check data files exist
   - Review logs

4. **404 Not Found**
   - Verify endpoint URL
   - Check round number exists
   - Review API documentation

## Test Checklist

- [ ] Server starts successfully
- [ ] Clients connect to server
- [ ] Health checks return 200
- [ ] Monitoring endpoints accessible
- [ ] Training can be triggered
- [ ] Metrics are recorded
- [ ] History is saved
- [ ] Summary statistics correct
- [ ] Multiple clients work simultaneously
- [ ] Error handling works correctly

## Continuous Testing

For continuous integration, create a test script that:

1. Starts server and clients
2. Waits for initialization
3. Runs all test suites
4. Collects results
5. Stops all processes
6. Reports results

See `scripts/run_full_training_with_monitoring.py` for an example of automated testing.

