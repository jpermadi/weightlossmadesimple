from fastapi import FastAPI, APIRouter
from typing import Optional
from app.models.schemas import BMI, BMI_value
from app.services import service_calculator_net
import asyncio


api_router = APIRouter()

# GET BMI value 
@api_router.get("/calculate-bmi/", status_code=200, response_model=BMI)
async def calculate_bmi(
    *,
    age: Optional[int] = 25,
    height_cm: int,
    weight_kg: int
) -> BMI:
    """
    Get BMI value and category from calculator.net
    """

    return await service_calculator_net.get_bmi(age=age, height_cm=height_cm, weight_kg=weight_kg)