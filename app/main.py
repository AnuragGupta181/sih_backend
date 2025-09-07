# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core import predictLca, lca_chat

app = FastAPI(title="LCA Backend API", version="1.0.0")


# ---------- Request/Response Models ----------
class LCAInput(BaseModel):
    Process_Type: str | None = None
    Metal: str | None = None
    Energy_MJ_per_kg: float | None = None
    Quantity_kg: float | None = None
    Energy_MJ_total: float | None = None
    Transport_km: float | None = None
    Transport_Mode: str | None = None
    Transport_emissions_kgCO2: float | None = None
    Water_use_m3_per_ton: float | None = None
    End_of_Life: str | None = None
    Circularity_option: str | None = None
    Process_emissions_kgCO2: float | None = None
    Total_emissions_kgCO2: float | None = None
    Emission_factor_kgCO2_per_MJ: float | None = None


class InsightRequest(BaseModel):
    sample_row: dict
    question: str


# ---------- Endpoints ----------
@app.get("/")
def root():
    return {"message": "Welcome to the LCA Backend API 🚀"}


@app.post("/predict")
def predict_lca(data: LCAInput):
    try:
        # Convert input to dict for model
        sample_row = data.dict()
        prediction = predictLca(sample_row)
        return {"predicted_data": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/insights")
def generate_insights(request: InsightRequest):
    try:
        insights = lca_chat(request.sample_row, request.question)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
