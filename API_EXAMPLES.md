# API Usage Examples

## Table of Contents

1. [Python Examples](#python-examples)
2. [JavaScript/Node.js Examples](#javascriptnodejs-examples)
3. [cURL Examples](#curl-examples)
4. [Real-world Scenarios](#real-world-scenarios)

## Python Examples

### Basic Monitoring

```python
import requests
import json
from datetime import datetime

# Server configuration
SERVER_URL = "http://localhost:8082"
CLIENT_URLS = [
    "http://localhost:8081",  # Client 1
    "http://localhost:8083",  # Client 2
    "http://localhost:8084"   # Client 3
]

def get_server_status():
    """Get server training status"""
    response = requests.get(f"{SERVER_URL}/monitoring/status")
    if response.status_code == 200:
        return response.json()
    return None

def get_client_status(client_url):
    """Get client status"""
    response = requests.get(f"{client_url}/monitoring/status")
    if response.status_code == 200:
        return response.json()
    return None

# Example usage
server_status = get_server_status()
print(f"Current round: {server_status['current_round']}")
print(f"Is training: {server_status['is_training']}")

for i, url in enumerate(CLIENT_URLS, 1):
    client_status = get_client_status(url)
    if client_status:
        print(f"Client {i}: {client_status['total_trainings']} trainings")
```

### Training Progress Monitor

```python
import requests
import time
from datetime import datetime

def monitor_training_progress(server_url, interval=5):
    """Monitor training progress in real-time"""
    print("Monitoring training progress...")
    print("Press Ctrl+C to stop\n")
    
    last_round = -1
    
    try:
        while True:
            # Get server status
            status = requests.get(f"{server_url}/monitoring/status").json()
            current_round = status.get("current_round")
            
            if current_round != last_round:
                last_round = current_round
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Round {current_round}")
                
                if status.get("is_training"):
                    # Get round details
                    round_details = requests.get(
                        f"{server_url}/monitoring/round/{current_round}"
                    ).json()
                    
                    if "aggregated_metrics" in round_details:
                        loss = round_details["aggregated_metrics"].get("loss")
                        print(f"  Loss: {loss:.6f}")
                    
                    # Show client participation
                    if "client_metrics" in round_details:
                        print(f"  Clients: {len(round_details['client_metrics'])}")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

# Usage
monitor_training_progress("http://localhost:8082")
```

### Update Training Configuration

```python
import requests

def update_training_config(client_url, local_epochs=5, learning_rate=0.001, batch_size=32):
    """Update training configuration for a client"""
    response = requests.post(
        f"{client_url}/train/trigger",
        json={
            "local_epochs": local_epochs,
            "learning_rate": learning_rate,
            "batch_size": batch_size
        }
    )
    
    if response.status_code == 200:
        print("Configuration updated successfully")
        print(json.dumps(response.json(), indent=2))
        return True
    elif response.status_code == 409:
        print("Training is already in progress")
        return False
    else:
        print(f"Error: {response.status_code}")
        return False

# Update all clients
for url in CLIENT_URLS:
    update_training_config(url, local_epochs=5, learning_rate=0.001)
```

### Export Training Metrics

```python
import requests
import json
import csv
from datetime import datetime

def export_training_metrics(server_url, output_file="training_metrics.json"):
    """Export all training metrics to JSON"""
    # Get history
    response = requests.get(f"{server_url}/monitoring/history?limit=1000")
    history = response.json()
    
    # Get summary
    summary_response = requests.get(f"{server_url}/monitoring/summary")
    summary = summary_response.json()
    
    # Combine data
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "summary": summary,
        "history": history.get("history", [])
    }
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"Exported {len(export_data['history'])} rounds to {output_file}")
    return export_data

def export_to_csv(server_url, output_file="training_metrics.csv"):
    """Export training metrics to CSV"""
    response = requests.get(f"{server_url}/monitoring/history?limit=1000")
    history = response.json().get("history", [])
    
    if not history:
        print("No history to export")
        return
    
    # Extract metrics
    rows = []
    for round_data in history:
        if round_data.get("status") == "completed":
            row = {
                "round": round_data.get("round"),
                "started_at": round_data.get("started_at"),
                "completed_at": round_data.get("completed_at"),
                "duration_seconds": round_data.get("duration_seconds"),
                "num_clients": round_data.get("num_clients"),
                "loss": round_data.get("aggregated_metrics", {}).get("loss")
            }
            rows.append(row)
    
    # Write CSV
    if rows:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"Exported {len(rows)} rounds to {output_file}")

# Export metrics
export_training_metrics("http://localhost:8082")
export_to_csv("http://localhost:8082")
```

### Compare Client Performance

```python
import requests
import pandas as pd

def compare_client_performance(client_urls):
    """Compare performance metrics across clients"""
    client_data = []
    
    for i, url in enumerate(client_urls, 1):
        try:
            # Get summary
            summary = requests.get(f"{url}/monitoring/summary").json()
            
            # Get status
            status = requests.get(f"{url}/monitoring/status").json()
            
            client_data.append({
                "client_id": i,
                "total_trainings": summary.get("total_trainings", 0),
                "average_loss": summary.get("average_training_loss"),
                "latest_loss": summary.get("latest_training_loss"),
                "min_loss": summary.get("min_training_loss"),
                "is_training": status.get("is_training", False)
            })
        except Exception as e:
            print(f"Error getting data for client {i}: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(client_data)
    print("\nClient Performance Comparison:")
    print(df.to_string(index=False))
    
    return df

# Compare clients
compare_client_performance(CLIENT_URLS)
```

## JavaScript/Node.js Examples

### Basic Monitoring Class

```javascript
const axios = require('axios');

class FlowerMonitor {
    constructor(serverUrl, clientUrls) {
        this.serverUrl = serverUrl;
        this.clientUrls = clientUrls;
    }
    
    async getServerStatus() {
        try {
            const response = await axios.get(`${this.serverUrl}/monitoring/status`);
            return response.data;
        } catch (error) {
            console.error('Error getting server status:', error.message);
            return null;
        }
    }
    
    async getClientStatus(clientIndex) {
        try {
            const url = this.clientUrls[clientIndex];
            const response = await axios.get(`${url}/monitoring/status`);
            return response.data;
        } catch (error) {
            console.error(`Error getting client ${clientIndex + 1} status:`, error.message);
            return null;
        }
    }
    
    async updateTrainingConfig(clientIndex, config) {
        try {
            const url = this.clientUrls[clientIndex];
            const response = await axios.post(`${url}/train/trigger`, config);
            return response.data;
        } catch (error) {
            console.error(`Error updating client ${clientIndex + 1} config:`, error.message);
            return null;
        }
    }
    
    async getTrainingHistory(limit = 10) {
        try {
            const response = await axios.get(
                `${this.serverUrl}/monitoring/history?limit=${limit}`
            );
            return response.data;
        } catch (error) {
            console.error('Error getting history:', error.message);
            return null;
        }
    }
}

// Usage
const monitor = new FlowerMonitor(
    'http://localhost:8082',
    ['http://localhost:8081', 'http://localhost:8083', 'http://localhost:8084']
);

// Get server status
monitor.getServerStatus().then(status => {
    console.log('Server Status:', status);
});

// Update client config
monitor.updateTrainingConfig(0, {
    local_epochs: 5,
    learning_rate: 0.001
}).then(result => {
    console.log('Config updated:', result);
});
```

### Real-time Dashboard (Node.js)

```javascript
const axios = require('axios');
const readline = require('readline');

class TrainingDashboard {
    constructor(serverUrl, clientUrls) {
        this.serverUrl = serverUrl;
        this.clientUrls = clientUrls;
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
    }
    
    async update() {
        // Clear screen
        process.stdout.write('\x1B[2J\x1B[0f');
        
        console.log('='.repeat(70));
        console.log('Flower Federated Learning Dashboard');
        console.log('='.repeat(70));
        console.log(`Time: ${new Date().toLocaleString()}\n`);
        
        // Server status
        try {
            const serverStatus = await axios.get(`${this.serverUrl}/monitoring/status`);
            const data = serverStatus.data;
            console.log('SERVER STATUS:');
            console.log(`  Current Round: ${data.current_round || 'N/A'}`);
            console.log(`  Total Rounds: ${data.total_rounds}`);
            console.log(`  Is Training: ${data.is_training}`);
            console.log(`  Uptime: ${data.uptime_seconds?.toFixed(1)}s\n`);
            
            // Server summary
            const summary = await axios.get(`${this.serverUrl}/monitoring/summary`);
            if (summary.data.latest_loss) {
                console.log('SERVER METRICS:');
                console.log(`  Latest Loss: ${summary.data.latest_loss.toFixed(6)}`);
                console.log(`  Average Loss: ${summary.data.average_loss?.toFixed(6) || 'N/A'}`);
                console.log(`  Min Loss: ${summary.data.min_loss?.toFixed(6) || 'N/A'}\n`);
            }
        } catch (error) {
            console.log('SERVER: Not available\n');
        }
        
        // Client statuses
        console.log('CLIENT STATUSES:');
        for (let i = 0; i < this.clientUrls.length; i++) {
            try {
                const status = await axios.get(`${this.clientUrls[i]}/monitoring/status`);
                const summary = await axios.get(`${this.clientUrls[i]}/monitoring/summary`);
                const statusData = status.data;
                const summaryData = summary.data;
                
                console.log(`  Client ${i + 1}:`);
                console.log(`    Trainings: ${statusData.total_trainings}`);
                console.log(`    Is Training: ${statusData.is_training}`);
                if (summaryData.latest_training_loss) {
                    console.log(`    Latest Loss: ${summaryData.latest_training_loss.toFixed(6)}`);
                }
            } catch (error) {
                console.log(`  Client ${i + 1}: Not available`);
            }
        }
        
        console.log('\n' + '='.repeat(70));
        console.log('Press Ctrl+C to exit');
    }
    
    start(interval = 2000) {
        this.update();
        setInterval(() => this.update(), interval);
    }
}

// Usage
const dashboard = new TrainingDashboard(
    'http://localhost:8082',
    ['http://localhost:8081', 'http://localhost:8083', 'http://localhost:8084']
);

dashboard.start(2000); // Update every 2 seconds
```

## cURL Examples

### Server Monitoring

```bash
# Health check
curl http://localhost:8082/health

# Get status
curl http://localhost:8082/monitoring/status | jq

# Get history (last 5 rounds)
curl "http://localhost:8082/monitoring/history?limit=5" | jq

# Get specific round details
curl http://localhost:8082/monitoring/round/5 | jq

# Get summary
curl http://localhost:8082/monitoring/summary | jq
```

### Client Operations

```bash
# Health check
curl http://localhost:8081/health | jq

# Get status
curl http://localhost:8081/status | jq

# Get model info
curl http://localhost:8081/model/info | jq

# Update training config
curl -X POST http://localhost:8081/train/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "local_epochs": 5,
    "learning_rate": 0.001,
    "batch_size": 32
  }' | jq

# Get monitoring status
curl http://localhost:8081/monitoring/status | jq

# Get training history
curl "http://localhost:8081/monitoring/history?limit=10" | jq

# Get metrics summary
curl http://localhost:8081/monitoring/summary | jq
```

### Batch Operations

```bash
# Check all clients
for port in 8081 8083 8084; do
  echo "Client on port $port:"
  curl -s http://localhost:$port/health | jq
  echo ""
done

# Get all client summaries
for port in 8081 8083 8084; do
  echo "Client on port $port summary:"
  curl -s http://localhost:$port/monitoring/summary | jq
  echo ""
done
```

## Real-world Scenarios

### Scenario 1: Monitor Training Session

```python
import requests
import time
from datetime import datetime

def monitor_training_session(server_url, duration_minutes=10):
    """Monitor a complete training session"""
    print(f"Monitoring training session for {duration_minutes} minutes...")
    print("=" * 70)
    
    start_time = time.time()
    rounds_completed = []
    
    while time.time() - start_time < duration_minutes * 60:
        try:
            status = requests.get(f"{server_url}/monitoring/status").json()
            current_round = status.get("current_round")
            
            if current_round and current_round not in rounds_completed:
                rounds_completed.append(current_round)
                
                # Get round details
                round_details = requests.get(
                    f"{server_url}/monitoring/round/{current_round}"
                ).json()
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Round {current_round}")
                
                if round_details.get("status") == "completed":
                    loss = round_details.get("aggregated_metrics", {}).get("loss")
                    duration = round_details.get("duration_seconds", 0)
                    print(f"  Completed in {duration:.2f}s")
                    print(f"  Loss: {loss:.6f}")
            
            time.sleep(5)
        
        except KeyboardInterrupt:
            break
    
    # Final summary
    summary = requests.get(f"{server_url}/monitoring/summary").json()
    print("\n" + "=" * 70)
    print("Session Summary:")
    print(f"  Rounds completed: {len(rounds_completed)}")
    print(f"  Latest loss: {summary.get('latest_loss', 'N/A')}")
    print(f"  Average loss: {summary.get('average_loss', 'N/A')}")

monitor_training_session("http://localhost:8082", duration_minutes=10)
```

### Scenario 2: Automated Training with Monitoring

```python
import requests
import time
import json

class AutomatedTrainingManager:
    """Manage automated training with monitoring"""
    
    def __init__(self, server_url, client_urls):
        self.server_url = server_url
        self.client_urls = client_urls
    
    def wait_for_training_completion(self, timeout=600):
        """Wait for current training to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = requests.get(f"{self.server_url}/monitoring/status").json()
            
            if not status.get("is_training"):
                return True
            
            time.sleep(5)
        
        return False
    
    def update_all_clients(self, config):
        """Update configuration for all clients"""
        results = []
        
        for i, url in enumerate(self.client_urls, 1):
            try:
                response = requests.post(f"{url}/train/trigger", json=config)
                if response.status_code == 200:
                    results.append({"client": i, "status": "updated"})
                else:
                    results.append({"client": i, "status": "failed", "code": response.status_code})
            except Exception as e:
                results.append({"client": i, "status": "error", "error": str(e)})
        
        return results
    
    def get_training_report(self):
        """Generate comprehensive training report"""
        report = {
            "server": {},
            "clients": []
        }
        
        # Server summary
        summary = requests.get(f"{self.server_url}/monitoring/summary").json()
        report["server"] = summary
        
        # Client summaries
        for i, url in enumerate(self.client_urls, 1):
            try:
                client_summary = requests.get(f"{url}/monitoring/summary").json()
                report["clients"].append({
                    "client_id": i,
                    "summary": client_summary
                })
            except:
                report["clients"].append({
                    "client_id": i,
                    "error": "Not available"
                })
        
        return report
    
    def run_training_cycle(self, config, wait_for_completion=True):
        """Run a complete training cycle"""
        print("Starting training cycle...")
        
        # Update all clients
        print("Updating client configurations...")
        update_results = self.update_all_clients(config)
        for result in update_results:
            print(f"  Client {result['client']}: {result['status']}")
        
        if wait_for_completion:
            print("\nWaiting for training to complete...")
            if self.wait_for_training_completion():
                print("Training completed!")
            else:
                print("Training timeout!")
        
        # Generate report
        print("\nGenerating report...")
        report = self.get_training_report()
        
        return report

# Usage
manager = AutomatedTrainingManager(
    "http://localhost:8082",
    ["http://localhost:8081", "http://localhost:8083", "http://localhost:8084"]
)

# Run training cycle
report = manager.run_training_cycle({
    "local_epochs": 5,
    "learning_rate": 0.001,
    "batch_size": 32
})

# Save report
with open("training_report.json", "w") as f:
    json.dump(report, f, indent=2)
```

### Scenario 3: Performance Analysis

```python
import requests
import matplotlib.pyplot as plt
import pandas as pd

def analyze_training_performance(server_url):
    """Analyze training performance and create visualizations"""
    # Get history
    response = requests.get(f"{server_url}/monitoring/history?limit=1000")
    history = response.json().get("history", [])
    
    if not history:
        print("No training history available")
        return
    
    # Extract data
    rounds = []
    losses = []
    durations = []
    
    for round_data in history:
        if round_data.get("status") == "completed":
            rounds.append(round_data.get("round"))
            losses.append(round_data.get("aggregated_metrics", {}).get("loss"))
            durations.append(round_data.get("duration_seconds"))
    
    # Create DataFrame
    df = pd.DataFrame({
        "round": rounds,
        "loss": losses,
        "duration": durations
    })
    
    # Create visualizations
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    
    # Loss over rounds
    axes[0].plot(df["round"], df["loss"], marker='o')
    axes[0].set_xlabel("Round")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Training Loss Over Rounds")
    axes[0].grid(True)
    
    # Duration over rounds
    axes[1].plot(df["round"], df["duration"], marker='s', color='green')
    axes[1].set_xlabel("Round")
    axes[1].set_ylabel("Duration (seconds)")
    axes[1].set_title("Round Duration Over Time")
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig("training_analysis.png")
    print("Analysis saved to training_analysis.png")
    
    # Print statistics
    print("\nTraining Statistics:")
    print(f"  Total rounds: {len(df)}")
    print(f"  Average loss: {df['loss'].mean():.6f}")
    print(f"  Min loss: {df['loss'].min():.6f}")
    print(f"  Max loss: {df['loss'].max():.6f}")
    print(f"  Average duration: {df['duration'].mean():.2f}s")
    
    return df

# Analyze performance
df = analyze_training_performance("http://localhost:8082")
```

### Scenario 4: Alert System

```python
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class TrainingAlertSystem:
    """Alert system for training anomalies"""
    
    def __init__(self, server_url, threshold_loss=0.1):
        self.server_url = server_url
        self.threshold_loss = threshold_loss
        self.last_round = -1
    
    def check_training_status(self):
        """Check for training issues"""
        try:
            status = requests.get(f"{self.server_url}/monitoring/status").json()
            current_round = status.get("current_round")
            
            if current_round and current_round != self.last_round:
                self.last_round = current_round
                
                # Get round details
                round_details = requests.get(
                    f"{self.server_url}/monitoring/round/{current_round}"
                ).json()
                
                if round_details.get("status") == "completed":
                    loss = round_details.get("aggregated_metrics", {}).get("loss")
                    
                    if loss and loss > self.threshold_loss:
                        self.send_alert(f"High loss detected: {loss:.6f} in round {current_round}")
                    
                    # Check for significant increase
                    if current_round > 1:
                        prev_round = requests.get(
                            f"{self.server_url}/monitoring/round/{current_round - 1}"
                        ).json()
                        prev_loss = prev_round.get("aggregated_metrics", {}).get("loss")
                        
                        if prev_loss and loss > prev_loss * 1.5:
                            self.send_alert(
                                f"Loss increased significantly: {prev_loss:.6f} -> {loss:.6f}"
                            )
        
        except Exception as e:
            self.send_alert(f"Error checking training status: {e}")
    
    def send_alert(self, message):
        """Send alert (implement email/SMS/etc.)"""
        print(f"[ALERT] {datetime.now()}: {message}")
        # Implement actual alert mechanism (email, SMS, webhook, etc.)

# Usage
alert_system = TrainingAlertSystem("http://localhost:8082", threshold_loss=0.1)

# Check periodically
import time
while True:
    alert_system.check_training_status()
    time.sleep(30)  # Check every 30 seconds
```

## Complete Integration Example

```python
import requests
import time
import json
from datetime import datetime

class FlowerAPIClient:
    """Complete API client for Flower federated learning"""
    
    def __init__(self, server_url, client_urls):
        self.server_url = server_url
        self.client_urls = client_urls
    
    # Server methods
    def get_server_status(self):
        return requests.get(f"{self.server_url}/monitoring/status").json()
    
    def get_server_history(self, limit=10):
        return requests.get(f"{self.server_url}/monitoring/history?limit={limit}").json()
    
    def get_server_summary(self):
        return requests.get(f"{self.server_url}/monitoring/summary").json()
    
    def get_round_details(self, round_num):
        return requests.get(f"{self.server_url}/monitoring/round/{round_num}").json()
    
    # Client methods
    def get_client_status(self, client_index):
        return requests.get(f"{self.client_urls[client_index]}/monitoring/status").json()
    
    def update_client_config(self, client_index, config):
        return requests.post(
            f"{self.client_urls[client_index]}/train/trigger",
            json=config
        ).json()
    
    def get_client_history(self, client_index, limit=20):
        return requests.get(
            f"{self.client_urls[client_index]}/monitoring/history?limit={limit}"
        ).json()
    
    # Utility methods
    def wait_for_training(self, timeout=600):
        """Wait for training to complete"""
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_server_status()
            if not status.get("is_training"):
                return True
            time.sleep(5)
        return False
    
    def get_all_statuses(self):
        """Get status from server and all clients"""
        return {
            "server": self.get_server_status(),
            "clients": [
                self.get_client_status(i) for i in range(len(self.client_urls))
            ]
        }

# Usage example
api = FlowerAPIClient(
    "http://localhost:8082",
    ["http://localhost:8081", "http://localhost:8083", "http://localhost:8084"]
)

# Get all statuses
all_statuses = api.get_all_statuses()
print(json.dumps(all_statuses, indent=2))

# Update all clients
for i in range(len(api.client_urls)):
    api.update_client_config(i, {
        "local_epochs": 5,
        "learning_rate": 0.001
    })

# Monitor training
api.wait_for_training()

# Get final summary
summary = api.get_server_summary()
print(f"Final loss: {summary.get('latest_loss')}")
```

For more examples and detailed API documentation, see `API_DOCUMENTATION.md`.

