# app/core/model_loader.py
"""
Handles loading of the trained Keras model and LabelEncoders.
"""

import pickle
import numpy as np
from keras.models import load_model
from app.models import LCAmodel


def load_model_and_encoders():
    """
    Loads the trained model and label encoders.
    """
    model = load_model(
        "app/models/LCA_value_predictor.keras",
        custom_objects={"LCAmodel": LCAmodel}
    )
    with open("app/models/LabelEncoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
    return model, label_encoders


# Load once at startup
model, LabelEncoders = load_model_and_encoders()


def encode_sample(sample_row: dict):
    """
    Encodes input data and creates mask array.
    """
    ld = []
    mask = []
    for key, val in sample_row.items():
        if val is not None:
            if key in LabelEncoders:
                if val in LabelEncoders[key].classes_:
                    encoded = LabelEncoders[key].transform([val])[0]
                else:
                    encoded = 0
                ld.append(encoded)
            else:
                ld.append(val)
            mask.append(1)
        else:
            ld.append(0.0)
            mask.append(0)
    return np.array(ld, dtype=np.float32), np.array(mask, dtype=np.float32)
