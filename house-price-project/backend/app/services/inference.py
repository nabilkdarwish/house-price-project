import logging

import joblib
import numpy as np

from app.core.config import settings
from app.schemas.prediction import PredictionRequest
from app.services.preprocessing import request_to_dataframe

logger = logging.getLogger(__name__)

_model = None


def load_model() -> None:
    """Load the trained pipeline once (called from the FastAPI lifespan on startup)."""
    global _model
    logger.info("Loading model from %s", settings.MODEL_PATH)
    _model = joblib.load(settings.MODEL_PATH)
    logger.info("Model loaded successfully")


def is_model_loaded() -> bool:
    return _model is not None


def predict_price(req: PredictionRequest) -> float:
    if _model is None:
        raise RuntimeError("Model is not loaded yet")

    X = request_to_dataframe(req)
    # The model was trained on log1p(price); invert with expm1 to get INR.
    pred_log = _model.predict(X)[0]
    pred_price = float(np.expm1(pred_log))
    return max(pred_price, 0.0)
