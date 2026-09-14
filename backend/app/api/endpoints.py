from typing import Any, Dict

from app.schemas.requests import PredictWeightRequest, RecommendRequest
from app.services.ml_service import ml_service
from fastapi import APIRouter

router = APIRouter()


@router.post("/recommend")
def recommend_exercises(request: RecommendRequest) -> Dict[str, Any]:
    """
    Get top K exercise recommendations based on history and user profile.
    """
    recommendations = ml_service.recommend(
        history_ids=request.history_ids, profile=request.profile, top_k=request.top_k
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
        raw_eq=request.raw_equipment,
    )

    eq = request.raw_equipment.lower()

    if "cardio" in eq or "fitness" in eq or "run" in eq or "bike" in eq:
        # Cardio exercises typically use time instead of weight
        # We can use the predicted "reps" as minutes, or just a placeholder
        target_text = f"{max(5, reps * 2)} mins"
    elif "bodyweight" in eq:
        if weight <= 0:
            target_text = f"Bodyweight x {reps} reps"
        else:
            target_text = f"+{weight} kg x {reps} reps"
    else:
        # Standard weights (Machine, Barbell, Dumbbell, Cable)
        if weight <= 0:
            target_text = f"Light Weight x {reps} reps"
        else:
            target_text = f"{weight} kg x {reps} reps"

    return {"weight": weight, "reps": reps, "target_text": target_text}
