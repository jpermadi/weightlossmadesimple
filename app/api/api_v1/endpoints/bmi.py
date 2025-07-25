from fastapi import APIRouter, Query, Form
from typing import Optional, Union, Annotated
from app.models.schemas import BMISearchResult, BMI, BMI_input
from app.data.bmi_data import BMI_DATA
from app.clients import calculator_net

router = APIRouter()


# ============================================================================= 77
# GET routes
# ============================================================================= 77
@router.get("/bmi-data/{id}", status_code=200, response_model=BMI)
def fetch_bmi_data(*, id: int) -> dict:
    """
    Fetch BMI data
    """

    for data in BMI_DATA:
        if data["id"] == id:
            return data


@router.get("/search-by-id/", status_code=200, response_model=Union[BMI, BMISearchResult])
def search_by_id(
    *,
    id: Optional[int] = None
) -> Union[BMI, BMISearchResult]:
    """
    Search for the BMI data of a customer based on ID
    """

    if not id:
        return BMISearchResult(results=[BMI(**data) for data in BMI_DATA])
    
    for data in BMI_DATA:
        if data["id"] == id:
            return BMI(**data)
        
        
@router.get("/search-by-category/", status_code=200, response_model=BMISearchResult)
def search_bmi(
    *,
    keyword:  Optional[str] = Query(
        None,   # Refers to the default value if user does not input anything
        min_length=3, 
        openapi_examples= {
            "BMIExample": {
                "description": "Search by weight category",
                "value": "Overweight"
            }
        }
        ),
        max_results: Optional[int] = 10
) -> BMISearchResult:
    """
    Get a list of BMIs based on category
    """
    
    if not keyword:
        return BMISearchResult(results=[BMI(**data) for data in BMI_DATA])

    else:
        temp_list = [BMI(**data) for data in BMI_DATA if keyword.lower() in data["category"].lower()]
        return BMISearchResult(results=temp_list)

# WITH WEBSCRAPING
@router.get("/calculate-bmi/", status_code=200, response_model=BMI)
async def calculate_bmi(
    *,
    age: int,
    height: int,
    weight: int
) -> BMI:
    """
    Get BMI value and category from calculator.net
    """

    return await calculator_net.get_bmi(age=age, height_cm=height, weight_kg=weight)

# WITH WEBSCRAPING
@router.post("/post-bmi/", status_code=201, response_model=BMI)
async def post_bmi(data: Annotated[BMI_input, Form()]) -> BMI:
    
    """
    Calculate BMI value and category from calculator.net then post the data with increment id
    """

    new_id = len(BMI_DATA) +1
    new_entry = await calculator_net.get_bmi(
        age=data.age, 
        height_cm=data.height, 
        weight_kg=data.weight
    )
    new_entry.id = new_id

    return new_entry