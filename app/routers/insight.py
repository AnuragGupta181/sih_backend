from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core import lca_chat
from app.core import predictLca

router = APIRouter(prefix="/insights", tags=["Insights"])


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


def predict_lca(data: LCAInput):
    sample_row = data.dict()
    print("Input LCA Data for Prediction:\n", sample_row)
    full_row = predictLca(sample_row)
    print("Predicted/Completed LCA Data:\n", full_row)
    return full_row


class InsightRequest(BaseModel):
    sample_row: LCAInput   
    question: str


@router.post("/")
def generate_insights(request: InsightRequest):
    try:
        
        insights = lca_chat(predict_lca(request.sample_row), request.question)
        print ("Generated Insights:\n", insights)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
