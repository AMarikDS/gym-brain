from typing import List, Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    sex: str
    age: float
    bw: float
    level: str  # Novice, Beginner, Intermediate, Advanced
    goal: str  # Powerbuilding, Bodybuilding, Athletics, Powerlifting, etc.
    equipment: str  # Machine, Dumbbell, Barbell, Bodyweight, All (Gym Mixed)
    sbd: Optional[List[float]] = [
        0.0,
        0.0,
        0.0,
    ]  # Squat, Bench, Deadlift (optional for LIGHT model)


class RecommendRequest(BaseModel):
    history_ids: List[int]
    profile: UserProfile
    top_k: int = 10


class PredictWeightRequest(BaseModel):
    profile: UserProfile
    exercise_name: str
    base_lift: Optional[str] = None
    raw_equipment: str = "Machine"
