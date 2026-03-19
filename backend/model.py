import joblib
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__), "../model/logistic.pkl")
model = joblib.load(model_path)

def predict_risk(features):
    X = np.array(features).reshape(1, -1)

    prob = model.predict_proba(X)[0][1]
    return prob
