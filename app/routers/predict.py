from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core import predictLca

router = APIRouter(prefix="/predict", tags=["Predict"])

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

@router.post("/")
# def predict_lca(data: LCAInput):
#     try:
#         sample_row = data.dict()
#         prediction = predictLca(sample_row)
#         return {"predicted_data": prediction}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

def predict_lca(data: LCAInput):
    try:
        sample_row = data.dict()
        print("🚀 Incoming request:", sample_row)  # Debug
        prediction = predictLca(sample_row)
        print("✅ Prediction:", prediction)  # Debug
        return {"predicted_data": prediction}
    except Exception as e:
        print("❌ Error in /predict:", e)  # Debug
        raise HTTPException(status_code=500, detail=str(e))