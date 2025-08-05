# Standard imports

# Third party imports
from fastapi import FastAPI, APIRouter, Query
from typing import Optional

# Local imports
from app.data.bmi_data import BMI_DATA
from app.models.schemas import BMI, BMISearchResult
from app.api.v1.api import api_router
from app.core.config import settings


# =============================================================================
# PROJECT INIT
# =============================================================================
app = FastAPI(title="Weight Loss Made Simple", openapi_url="/openapi.json")
root_router = APIRouter()


# Root route (GET "/") 
@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


# =============================================================================
# INCLUDE ROUTES
# =============================================================================
app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_V1_STR)

# Used only for development purpose
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")