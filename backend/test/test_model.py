import pandas as pd
import joblib
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__), "../../model/logistic.pkl")
model = joblib.load(model_path)

columns = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

np.random.seed(None)

normal_v = np.random.randn(3, 28)
normal_time = np.random.uniform(0, 172792, (3, 1))
normal_amount = np.random.uniform(1, 200, (3, 1))
normal_data = np.hstack([normal_time, normal_v, normal_amount])

fraud_v = np.random.randn(2, 28)
fraud_v[:, 0] *= -4    
fraud_v[:, 3] *= 4     
fraud_v[:, 9] *= -3    
fraud_v[:, 11] *= -4   
fraud_v[:, 13] *= -4   
fraud_time = np.random.uniform(0, 172792, (2, 1))
fraud_amount = np.random.uniform(200, 2000, (2, 1))
fraud_data = np.hstack([fraud_time, fraud_v, fraud_amount])

all_data = np.vstack([normal_data, fraud_data])
labels = ["normal"] * 3 + ["fraud"] * 2
shuffle_idx = np.random.permutation(5)
all_data = all_data[shuffle_idx]
labels = [labels[i] for i in shuffle_idx]

sample = pd.DataFrame(all_data, columns=columns)

for i in range(len(sample)):
    print(f"Sample {i+1} [{labels[i]}]: Time={sample['Time'][i]:.0f}, Amount={sample['Amount'][i]:.2f}")

pred_proba = model.predict_proba(sample)[:, 1]
pred_class = model.predict(sample)

for i in range(len(sample)):
    print(f"Sample {i+1}: Risk score={pred_proba[i]:.3f}, Predicted class={pred_class[i]} (expected: {labels[i]})")
