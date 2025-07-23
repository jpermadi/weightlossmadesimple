# Import necessary modules and classes (FastAPI, Pydantic, etc.)
from fastapi import FastAPI, APIRouter, Query
from typing import Optional
from app.data.bmi_data import BMI_DATA
from app.models.schemas import BMI, BMISearchResult, BMI_input
from app.api.routes import route_calculator_net


app = FastAPI(title="Weight Loss Made Simple", openapi_url="/openapi.json")
api_router = APIRouter()



# Root route (GET "/") 
@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}

# POST route to create a new item
# - Validate the incoming request
# - Add it to the database
# - Return a response with the new item
@api_router.post("/post-bmi/", status_code=201, response_model=BMI)
def post_bmi(
    *,
    age: int,
    height_cm: int,
    weight_kg: int
) -> BMI:
    
    new_id = len(BMI_DATA) +1
    new_entry = BMI(
        id=new_id,
        age=age,
        height= height_cm,
        weight= weight_kg
    )

    return new_entry


# GET route to return all items
# - Return the full list of stored items
@api_router.get("/search-by-category/", status_code=200, response_model=BMISearchResult)
def search_bmi(
    *,
    keyword:  Optional[str] = Query(
        None,   # Refers to the default value if user does not input anything
        min_length=3, 
        openapi_examples= {
            "BMIExample": {
                "category": "Your belong to the overweight category",
                "value": "overweight"
            }
        }
        ),
        max_results: Optional[int] = 10
) -> dict:
    """
    Get a list of BMIs based on category
    """
    if not keyword:
        return {"results": BMI_DATA[:max_results]}

    temp_list = []
    for data in BMI_DATA:
        if keyword.lower() in data["category"].lower():
            temp_list.append(data)
    
    return {"results": temp_list}

# GET route to return a specific item by ID
# - Look up the item
# - Return it if found
# - Raise a 404 if not found
@api_router.get("/bmi-data/{id}", status_code=200, response_model=BMI)
def fetch_bmi_data(*, id: int) -> dict:
    """
    Fetch BMI data
    """

    for data in BMI_DATA:
        if data["id"] == id:
            return data

@api_router.get("/search-by-id/", status_code=200, response_model=BMI)
def search_by_id(
    *,
    id: Optional[int] = None, 
    category: Optional[str] = None, 
    max_result: Optional[int] = 10
) -> dict:
    """
    Search for the BMI data of a customer based on ID
    """
    if not id:
        return {"results": BMI_DATA[:max_result]}
    
    for data in BMI_DATA:
        if data["id"] == id:
            return {"results": data}

# DELETE route to remove an item by ID
# - Find the item and remove it
# - Return a success message or 404 if not found

app.include_router(api_router)
app.include_router(route_calculator_net.api_router)

# Used only for development purpose
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")