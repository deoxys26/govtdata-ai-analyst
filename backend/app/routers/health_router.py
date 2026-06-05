from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "GovData AI Analyst backend is running"
    }
