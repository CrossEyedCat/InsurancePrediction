"""
Patient management API endpoints
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medical_worker import MedicalWorker
from app.models.patient import Patient
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
)
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[PatientResponse])
async def list_patients(
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user),
):
    query = db.query(Patient)
    if current_user.role.value != "admin":
        query = query.filter(
            Patient.institution_id == current_user.institution_id
        )
    patients = query.all()
    return patients


@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user),
):
    data = patient_in.dict()
    data["institution_id"] = current_user.institution_id

    patient = Patient(**data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    if (
        current_user.role.value != "admin"
        and patient.institution_id != current_user.institution_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this patient",
        )

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    if (
        current_user.role.value != "admin"
        and patient.institution_id != current_user.institution_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this patient",
        )

    update_data = patient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: MedicalWorker = Depends(get_current_user),
):
    
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    # Check access
    if (
        current_user.role.value != "admin"
        and patient.institution_id != current_user.institution_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this patient",
        )

    db.delete(patient)
    db.commit()
    return None
