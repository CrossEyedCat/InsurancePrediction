from fastapi import APIRouter
from app.api import auth, patients
from app.api import predictions

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(patients.router)
api_router.include_router(predictions.router)
