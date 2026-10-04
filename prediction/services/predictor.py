import joblib
import pandas as pd
from django.conf import settings


MODEL_PATH = (
    settings.BASE_DIR
    / "ml"
    / "models"
    / "concrete_strength_model.joblib"
)

model = joblib.load(MODEL_PATH)


FEATURES = [
    "cement",
    "blast_furnace_slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age",
]


def predict_strength(data):
    input_data = pd.DataFrame(
        [[data[feature] for feature in FEATURES]],
        columns=FEATURES,
    )

    prediction = model.predict(input_data)

    return float(prediction[0])