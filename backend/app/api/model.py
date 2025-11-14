"""
Model management API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.medical_worker import MedicalWorker
from app.models.model_version import ModelVersion
from app.models.training_round import TrainingRound
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/status")
async def get_model_status(
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user)
):
    """Get current model status"""
    active_model = db.query(ModelVersion).filter(ModelVersion.is_active == True).first()
    if not active_model:
        return {"status": "no_model", "message": "No active model available"}
    
    return {
        "status": "active",
        "version": active_model.version,
        "accuracy": float(active_model.accuracy) if active_model.accuracy else None,
        "mse": float(active_model.mse) if active_model.mse else None,
        "mae": float(active_model.mae) if active_model.mae else None,
        "trained_at": active_model.trained_at.isoformat() if active_model.trained_at else None
    }


@router.get("/metrics")
async def get_model_metrics(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user)
):
    """Get training round metrics"""
    rounds = db.query(TrainingRound).order_by(TrainingRound.round_number.desc()).limit(limit).all()
    
    return {
        "rounds": [
            {
                "round_number": r.round_number,
                "status": r.status,
                "clients_participated": r.clients_participated,
                "metrics": r.metrics,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None
            }
            for r in rounds
        ]
    }

