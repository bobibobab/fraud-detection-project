import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import os

dataset_path = os.path.join(os.path.dirname(__file__), "../data")

csv_file = os.path.join(dataset_path, "creditcard.csv")

df = pd.read_csv(csv_file)

X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000))
])
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["normal", "fraud"]))

# --- Fraud class (Class=1) metrics across training sizes ---
from sklearn.metrics import precision_score, recall_score, f1_score

train_sizes_list = np.linspace(0.1, 1.0, 8)
precisions, recalls, f1s = [], [], []

for frac in train_sizes_list:
    n = int(len(X_train) * frac)
    X_sub, y_sub = X_train.iloc[:n], y_train.iloc[:n]
    m = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))])
    m.fit(X_sub, y_sub)
    y_p = m.predict(X_test)
    precisions.append(precision_score(y_test, y_p, zero_division=0))
    recalls.append(recall_score(y_test, y_p, zero_division=0))
    f1s.append(f1_score(y_test, y_p, zero_division=0))

sizes = (train_sizes_list * len(X_train)).astype(int)

plt.figure(figsize=(10, 6))
plt.plot(sizes, precisions, label="Precision (fraud)", color="blue",   marker="o")
plt.plot(sizes, recalls,    label="Recall (fraud)",    color="orange",  marker="s")
plt.plot(sizes, f1s,        label="F1 Score (fraud)",  color="green",   marker="^")
plt.title("Model Performance on Fraud Class vs Training Size")
plt.xlabel("Training Set Size")
plt.ylabel("Score")
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True)
plt.tight_layout()

graph_path = os.path.join(os.path.dirname(__file__), "../model/learning_curve.png")
plt.savefig(graph_path)
plt.show()
print(f"Graph saved to {graph_path}")

model_path = os.path.join(os.path.dirname(__file__), "../model/logistic.pkl")
joblib.dump(model, model_path)

print("Model saved")
