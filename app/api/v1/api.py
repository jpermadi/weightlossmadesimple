from fastapi import APIRouter
from app.api.v1.endpoints import endpoint_calculator_net, bmi

api_router = APIRouter()
# api_router.include_router(endpoint_calculator_net.router, prefix="/bmi", tags=["bmi"])
api_router.include_router(bmi.router, prefix="/bmi", tags=["bmi"])