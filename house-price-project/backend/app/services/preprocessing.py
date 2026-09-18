import json
from functools import lru_cache
from pathlib import Path

import pandas as pd

from app.core.config import settings
from app.schemas.prediction import PredictionRequest

NUMERIC_FEATURES = ["carpet_area_sqft", "floor_num", "bathroom", "balcony"]
CATEGORICAL_FEATURES = ["location_grouped", "Furnishing", "Transaction", "Ownership", "facing"]


@lru_cache(maxsize=1)
def get_known_locations() -> set[str]:
    path = Path(settings.LOCATIONS_PATH)
    if not path.exists():
        return set()
    with open(path) as f:
        return set(json.load(f))


def request_to_dataframe(req: PredictionRequest) -> pd.DataFrame:
    """Build a single-row DataFrame with exactly the column names used at training time.

    Because the exported model is a full sklearn Pipeline (ColumnTransformer + estimator),
    no manual encoding/scaling is needed here — the pipeline handles it.
    """
    known_locations = get_known_locations()
    location = req.location if req.location in known_locations else "other"

    row = {
        "carpet_area_sqft": req.carpet_area_sqft,
        "floor_num": req.floor_num,
        "bathroom": req.bathroom,
        "balcony": req.balcony,
        "location_grouped": location,
        "Furnishing": req.furnishing or "Unknown",
        "Transaction": req.transaction or "Unknown",
        "Ownership": req.ownership or "Unknown",
        "facing": req.facing or "Unknown",
    }
    return pd.DataFrame([row], columns=NUMERIC_FEATURES + CATEGORICAL_FEATURES)
