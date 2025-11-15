"""
Monitoring system for Flower client
Tracks local training metrics and progress
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import threading


class ClientMonitor:
    """Monitor for Flower client training metrics"""
    
    def __init__(self, client_id: int, log_dir: str = "monitoring"):
        self.client_id = client_id
        self.log_dir = Path(log_dir) / f"client_{client_id}"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Training history
        self.training_history: List[Dict] = []
        self.current_training: Optional[Dict] = None
        
        # Statistics
        self.total_trainings = 0
        self.total_evaluations = 0
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
                    self.total_trainings = data.get("total_trainings", 0)
                    self.total_evaluations = data.get("total_evaluations", 0)
            except Exception as e:
                print(f"Warning: Could not load training history: {e}")
    
    def _save_history(self):
        """Save training history to file"""
        history_file = self.log_dir / "training_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump({
                    "client_id": self.client_id,
                    "history": self.training_history,
                    "total_trainings": self.total_trainings,
                    "total_evaluations": self.total_evaluations,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save training history: {e}")
    
    def start_training(self, round_num: int, config: Dict):
        """Record start of training"""
        with self.lock:
            self.current_training = {
                "round": round_num,
                "started_at": datetime.now().isoformat(),
                "config": config,
                "status": "training"
            }
            self.total_trainings += 1
    
    def record_training_metrics(self, round_num: int, loss: float, num_samples: int, 
                               local_epochs: int, duration: float):
        """Record training metrics"""
        with self.lock:
            training_record = {
                "round": round_num,
                "type": "training",
                "loss": loss,
                "num_samples": num_samples,
                "local_epochs": local_epochs,
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat()
            }
            
            self.training_history.append(training_record)
            
            # Update current training
            if self.current_training and self.current_training["round"] == round_num:
                self.current_training.update({
                    "loss": loss,
                    "num_samples": num_samples,
                    "duration_seconds": duration,
                    "status": "completed"
                })
                self.current_training = None
            
            # Keep only last 100 records in memory
            if len(self.training_history) > 100:
                self.training_history = self.training_history[-100:]
            
            # Save to file
            self._save_history()
    
    def record_evaluation_metrics(self, round_num: int, loss: float, mse: float, 
                                  num_samples: int, duration: float):
        """Record evaluation metrics"""
        with self.lock:
            eval_record = {
                "round": round_num,
                "type": "evaluation",
                "loss": loss,
                "mse": mse,
                "rmse": mse ** 0.5,
                "num_samples": num_samples,
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat()
            }
            
            self.training_history.append(eval_record)
            self.total_evaluations += 1
            
            # Keep only last 100 records in memory
            if len(self.training_history) > 100:
                self.training_history = self.training_history[-100:]
            
            # Save to file
            self._save_history()
    
    def get_current_status(self) -> Dict:
        """Get current training status"""
        with self.lock:
            return {
                "client_id": self.client_id,
                "current_training": self.current_training,
                "total_trainings": self.total_trainings,
                "total_evaluations": self.total_evaluations,
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "is_training": self.current_training is not None
            }
    
    def get_training_history(self, limit: int = 20) -> List[Dict]:
        """Get recent training history"""
        with self.lock:
            return self.training_history[-limit:]
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of training metrics"""
        with self.lock:
            training_records = [r for r in self.training_history if r.get("type") == "training"]
            eval_records = [r for r in self.training_history if r.get("type") == "evaluation"]
            
            if not training_records:
                return {"message": "No training records available"}
            
            training_losses = [r["loss"] for r in training_records if "loss" in r]
            eval_losses = [r["loss"] for r in eval_records if "loss" in r]
            
            return {
                "total_trainings": len(training_records),
                "total_evaluations": len(eval_records),
                "average_training_loss": sum(training_losses) / len(training_losses) if training_losses else None,
                "average_eval_loss": sum(eval_losses) / len(eval_losses) if eval_losses else None,
                "min_training_loss": min(training_losses) if training_losses else None,
                "min_eval_loss": min(eval_losses) if eval_losses else None,
                "latest_training_loss": training_losses[-1] if training_losses else None,
                "latest_eval_loss": eval_losses[-1] if eval_losses else None
            }


# Global monitor instances per client
_monitor_instances: Dict[int, ClientMonitor] = {}


def get_monitor(client_id: int) -> ClientMonitor:
    """Get monitor instance for a client"""
    if client_id not in _monitor_instances:
        log_dir = os.getenv("MONITORING_DIR", "monitoring")
        _monitor_instances[client_id] = ClientMonitor(client_id, log_dir)
    return _monitor_instances[client_id]

