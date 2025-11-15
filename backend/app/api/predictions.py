"""
Prediction API endpoints
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medical_worker import MedicalWorker
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.api.auth import get_current_user
from app.services.prediction_service import PredictionService

router = APIRouter()


@router.post("/", response_model=PredictionResponse)
async def predict_insurance_cost(
    prediction_request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user),
):
    try:
        prediction_service = PredictionService()

        predicted_cost = await prediction_service.predict(
            prediction_request.dict()
        )

        return PredictionResponse(
            predicted_cost=predicted_cost,
            model_version=prediction_service.get_active_model_version(),
            prediction_timestamp=datetime.utcnow(),
            patient_id=prediction_request.patient_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
