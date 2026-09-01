from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="Gym Brain ML API", 
    version="1.0.0",
    description="Machine Learning backend for Gym Brain Recommender System"
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
