from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

API_VERSION = "1.0.0"

@router.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "LCA Backend API is running 🚀",
        "version": API_VERSION
    }
