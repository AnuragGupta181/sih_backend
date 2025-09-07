# app/core/predictor.py
"""
Prediction logic using the trained ML model.
"""

import numpy as np
from app.core.model_loader import model, LabelEncoders, encode_sample


def predictLca(sample_row: dict) -> dict:
    """
    Predicts missing values in the given LCA input data.
    """
    X, mask = encode_sample(sample_row)

    X_input = X.reshape(1, -1)
    mask_input = mask.reshape(1, -1)
    pred = model.predict([X_input, mask_input])

    result = {}
    columns = [
        "Process_Type",
        "Metal",
        "Energy_MJ_per_kg",
        "Quantity_kg",
        "Energy_MJ_total",
        "Transport_km",
        "Transport_Mode",
        "Transport_emissions_kgCO2",
        "Water_use_m3_per_ton",
        "End_of_Life",
        "Circularity_option",
        "Process_emissions_kgCO2",
        "Total_emissions_kgCO2",
        "Emission_factor_kgCO2_per_MJ"
    ]

    for i, m, v in zip(columns, mask, pred[0]):
        if m != 0:  # keep original if provided
            result[i] = sample_row[i]
        else:  # predict missing
            if i in LabelEncoders:
                v = int(round(v))
                if v < 0:
                    v = 0
                inv = LabelEncoders[i].inverse_transform([v])[0]
                result[i] = inv
            else:
                result[i] = round(float(v), 2)

    return result
