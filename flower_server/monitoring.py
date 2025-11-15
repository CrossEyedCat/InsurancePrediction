"""
Monitoring system for Flower server
Tracks training metrics, rounds, and client participation
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import threading


class ServerMonitor:
    """Monitor for Flower server training metrics"""
    
    def __init__(self, log_dir: str = "monitoring"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Training history
        self.training_history: List[Dict] = []
        self.current_round: Optional[int] = None
        self.round_start_time: Optional[datetime] = None
        
        # Metrics storage
        self.round_metrics: Dict[int, Dict] = {}
        self.client_metrics: Dict[int, List[Dict]] = defaultdict(list)
        
        # Statistics
        self.total_rounds = 0
        self.total_clients = 0
        self.start_time = datetime.now()
        
        # Lock for thread safety
        self.lock = threading.Lock()
        
        # Load existing history
        self._load_history()
    
    def _load_history(self):
        """Load training history from file"""
        history_file = self.log_dir / "training_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.training_history = data.get("history", [])
                    self.total_rounds = data.get("total_rounds", 0)
                    self.total_clients = data.get("total_clients", 0)
            except Exception as e:
                print(f"Warning: Could not load training history: {e}")
    
    def _save_history(self):
        """Save training history to file"""
        history_file = self.log_dir / "training_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump({
                    "history": self.training_history,
                    "total_rounds": self.total_rounds,
                    "total_clients": self.total_clients,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save training history: {e}")
    
    def start_round(self, round_num: int, num_clients: int = 0):
        """Record start of a training round"""
        with self.lock:
            self.current_round = round_num
            self.round_start_time = datetime.now()
            self.total_rounds = max(self.total_rounds, round_num)
            self.total_clients = max(self.total_clients, num_clients)
            
            round_info = {
                "round": round_num,
                "started_at": self.round_start_time.isoformat(),
                "num_clients": num_clients,
                "status": "in_progress"
            }
            
            self.round_metrics[round_num] = round_info
            print(f"[Monitor] Round {round_num} started with {num_clients} clients")
    
    def record_fit_metrics(self, round_num: int, client_id: int, metrics: Dict, num_samples: int):
        """Record metrics from a client fit"""
        with self.lock:
            client_metric = {
                "round": round_num,
                "client_id": client_id,
                "num_samples": num_samples,
                "metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
            
            self.client_metrics[round_num].append(client_metric)
            
            # Update round metrics
            if round_num in self.round_metrics:
                if "client_metrics" not in self.round_metrics[round_num]:
                    self.round_metrics[round_num]["client_metrics"] = []
                self.round_metrics[round_num]["client_metrics"].append(client_metric)
    
    def record_eval_metrics(self, round_num: int, client_id: int, metrics: Dict, num_samples: int):
        """Record metrics from a client evaluation"""
        with self.lock:
            # Find existing client metric for this round
            for metric in self.client_metrics[round_num]:
                if metric["client_id"] == client_id:
                    metric["eval_metrics"] = metrics
                    metric["eval_samples"] = num_samples
                    break
    
    def complete_round(self, round_num: int, aggregated_metrics: Optional[Dict] = None):
        """Record completion of a training round"""
        with self.lock:
            if round_num not in self.round_metrics:
                return
            
            end_time = datetime.now()
            duration = (end_time - self.round_start_time).total_seconds() if self.round_start_time else None
            
            round_info = self.round_metrics[round_num].copy()
            round_info.update({
                "completed_at": end_time.isoformat(),
                "duration_seconds": duration,
                "status": "completed",
                "aggregated_metrics": aggregated_metrics or {}
            })
            
            # Add to history
            self.training_history.append(round_info)
            
            # Keep only last 100 rounds in memory
            if len(self.training_history) > 100:
                self.training_history = self.training_history[-100:]
            
            # Save to file
            self._save_history()
            
            print(f"[Monitor] Round {round_num} completed in {duration:.2f}s")
            if aggregated_metrics:
                print(f"[Monitor] Aggregated metrics: {aggregated_metrics}")
    
    def get_current_status(self) -> Dict:
        """Get current training status"""
        with self.lock:
            return {
                "current_round": self.current_round,
                "round_start_time": self.round_start_time.isoformat() if self.round_start_time else None,
                "total_rounds": self.total_rounds,
                "total_clients": self.total_clients,
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "is_training": self.current_round is not None
            }
    
    def get_round_history(self, limit: int = 10) -> List[Dict]:
        """Get recent training rounds"""
        with self.lock:
            return self.training_history[-limit:]
    
    def get_round_details(self, round_num: int) -> Optional[Dict]:
        """Get detailed information about a specific round"""
        with self.lock:
            return self.round_metrics.get(round_num)
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of all metrics"""
        with self.lock:
            if not self.training_history:
                return {"message": "No training history available"}
            
            # Calculate statistics
            completed_rounds = [r for r in self.training_history if r.get("status") == "completed"]
            
            if not completed_rounds:
                return {"message": "No completed rounds yet"}
            
            # Extract loss values
            losses = []
            for round_info in completed_rounds:
                metrics = round_info.get("aggregated_metrics", {})
                if "loss" in metrics:
                    losses.append(metrics["loss"])
            
            return {
                "total_rounds": len(completed_rounds),
                "average_loss": sum(losses) / len(losses) if losses else None,
                "min_loss": min(losses) if losses else None,
                "max_loss": max(losses) if losses else None,
                "latest_round": completed_rounds[-1]["round"] if completed_rounds else None,
                "latest_loss": losses[-1] if losses else None
            }


# Global monitor instance
_monitor_instance: Optional[ServerMonitor] = None


def get_monitor() -> ServerMonitor:
    """Get global monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        log_dir = os.getenv("MONITORING_DIR", "monitoring")
        _monitor_instance = ServerMonitor(log_dir)
    return _monitor_instance

