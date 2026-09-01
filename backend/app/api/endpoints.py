from fastapi import APIRouter
from typing import Dict, Any

from app.schemas.requests import RecommendRequest, PredictWeightRequest
from app.services.ml_service import ml_service

router = APIRouter()

@router.post("/recommend")
def recommend_exercises(request: RecommendRequest) -> Dict[str, Any]:
    """
    Get top K exercise recommendations based on history and user profile.
    """
    recommendations = ml_service.recommend(
        history_ids=request.history_ids,
        profile=request.profile,
        top_k=request.top_k
    )
    return {"recommendations": recommendations}

@router.post("/predict_weight")
def predict_weight(request: PredictWeightRequest) -> Dict[str, Any]:
    """
    Predict optimal weight and reps for a given exercise and profile.
    """
    weight, reps = ml_service.predict_weight(
        profile=request.profile,
        exercise_name=request.exercise_name,
        base_lift=request.base_lift,
        raw_eq=request.raw_equipment
    )
    return {"weight": weight, "reps": reps}
