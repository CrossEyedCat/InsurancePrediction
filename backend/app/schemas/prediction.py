"""
Prediction schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class PredictionRequest(BaseModel):
    """Prediction request schema"""
    age: int = Field(..., ge=0, le=150)
    sex: str = Field(..., pattern="^(male|female)$")
    bmi: Optional[Decimal] = Field(None, ge=0, le=100)
    children: int = Field(0, ge=0)
    smoker: str = Field("no", pattern="^(yes|no)$")
    region: Optional[str] = None
    patient_id: Optional[int] = None  # Optional: link to patient record


class PredictionResponse(BaseModel):
    """Prediction response schema"""
    predicted_cost: Decimal
    confidence: Optional[float] = None
    model_version: Optional[str] = None
    prediction_timestamp: datetime
    patient_id: Optional[int] = None

