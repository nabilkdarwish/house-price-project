from typing import Optional

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    location: str = Field(..., min_length=1, description="Locality, e.g. 'Sector 12, Noida'")
    carpet_area_sqft: float = Field(..., gt=0, description="Carpet area in square feet")
    floor_num: int = Field(..., ge=-1, le=200, description="Floor number (0 = Ground, -1 = Basement)")
    bathroom: int = Field(..., ge=0, le=20)
    balcony: int = Field(..., ge=0, le=20)
    furnishing: str = Field(..., description='"Furnished" | "Semi-Furnished" | "Unfurnished"')
    transaction: str = Field(..., description='"New Property" | "Resale"')
    ownership: str = Field(..., description='e.g. "Freehold", "Leasehold"')
    facing: Optional[str] = Field(None, description='e.g. "East", "North-West"')

    model_config = {
        "json_schema_extra": {
            "example": {
                "location": "Sector 12, Noida",
                "carpet_area_sqft": 1200,
                "floor_num": 3,
                "bathroom": 2,
                "balcony": 1,
                "furnishing": "Semi-Furnished",
                "transaction": "Resale",
                "ownership": "Freehold",
                "facing": "East",
            }
        }
    }


class PredictionResponse(BaseModel):
    predicted_price: float


class HealthResponse(BaseModel):
    status: str
