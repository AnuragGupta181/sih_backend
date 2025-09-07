from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core import lca_chat

router = APIRouter(prefix="/insights", tags=["Insights"])

class InsightRequest(BaseModel):
    sample_row: dict
    question: str

@router.post("/")
def generate_insights(request: InsightRequest):
    try:
        insights = lca_chat(request.sample_row, request.question)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
