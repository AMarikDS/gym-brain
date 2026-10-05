from typing import Any, Dict

from app.schemas.requests import PredictWeightRequest, RecommendRequest
from app.services.ml_service import ml_service
from app.services.translation_service import translation_service
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

    if request.language == "ru":
        for rec in recommendations:
            rec["translated_name"] = translation_service.translate_en_to_ru(rec["exercise_name"])
    else:
        for rec in recommendations:
            rec["translated_name"] = rec["exercise_name"]

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
        if request.language == "ru":
            target_text = f"{max(5, reps * 2)} минут"
        else:
            target_text = f"{max(5, reps * 2)} minutes"
    elif "bodyweight" in eq:
        if weight <= 0:
            if request.language == "ru":
                target_text = f"Свой вес x {reps} повторений"
            else:
                target_text = f"Bodyweight x {reps} repetitions"
        else:
            if request.language == "ru":
                target_text = f"+{weight} килограмм x {reps} повторений"
            else:
                target_text = f"+{weight} kilograms x {reps} repetitions"
    else:
        # Standard weights (Machine, Barbell, Dumbbell, Cable)
        if weight <= 0:
            if request.language == "ru":
                target_text = f"Легкий вес x {reps} повторений"
            else:
                target_text = f"Light Weight x {reps} repetitions"
        else:
            if request.language == "ru":
                target_text = f"{weight} килограмм x {reps} повторений"
            else:
                target_text = f"{weight} kilograms x {reps} repetitions"

    return {"weight": weight, "reps": reps, "target_text": target_text}
