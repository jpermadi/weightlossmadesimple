from pydantic import BaseModel
from typing import Sequence, Optional

class BMI_input(BaseModel):
    age: int
    height: int
    weight: int

class BMI(BMI_input):
    id: Optional[int] = None
    age: int
    height: int
    weight: int
    bmi: Optional[float] = None
    category: Optional[str] = None

class BMISearchResult(BaseModel):
    results: Sequence[BMI]

class BMI_value(BaseModel):
    age: int
    height: int
    weight: int
    bmi: float
    category: str
