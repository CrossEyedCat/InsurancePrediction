"""
Patient schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PatientBase(BaseModel):
    """Base patient schema"""
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    age: int = Field(..., ge=0, le=150)
    sex: str = Field(..., pattern="^(male|female)$")
    bmi: Optional[Decimal] = Field(None, ge=0, le=100)
    children: int = Field(0, ge=0)
    smoker: str = Field("no", pattern="^(yes|no)$")
    region: Optional[str] = None
    insurance_cost: Optional[Decimal] = None  # For training data


class PatientCreate(PatientBase):
    """Patient creation schema"""
    pass


class PatientUpdate(BaseModel):
    """Patient update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    sex: Optional[str] = Field(None, pattern="^(male|female)$")
    bmi: Optional[Decimal] = Field(None, ge=0, le=100)
    children: Optional[int] = Field(None, ge=0)
    smoker: Optional[str] = Field(None, pattern="^(yes|no)$")
    region: Optional[str] = None
    insurance_cost: Optional[Decimal] = None


class PatientResponse(PatientBase):
    """Patient response schema"""
    id: int
    institution_id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

