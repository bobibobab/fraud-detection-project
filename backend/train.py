import pandas as pd
from sklearn.model_selection import train_test_split
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

model_path = os.path.join(os.path.dirname(__file__), "../model/logistic.pkl")
joblib.dump(model, model_path)

print("Model saved")
