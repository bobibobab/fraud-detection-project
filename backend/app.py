from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .model import predict_risk
from .rule_engine import apply_rules
from .feature_eng import build_feature_vector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 엔드포인트 (raw feature vector 입력)
@app.post("/check")
def predict(features: dict):
    features = features["features"]
    amount = features["amount"]
    risk = predict_risk(features)
    risk, decision = apply_rules(amount, risk)
    return {"risk_score": risk, "decision": decision}


# 새 엔드포인트 (유저 결제 정보 입력)
class PaymentRequest(BaseModel):
    amount: float
    merchant_category: str   # food, shopping, travel, entertainment, medical, other
    is_overseas: bool
    is_new_merchant: bool
    transaction_time: str    # "HH:MM" 형식

@app.post("/payment")
def payment_check(req: PaymentRequest):
    features = build_feature_vector(
        amount=req.amount,
        merchant_category=req.merchant_category,
        is_overseas=req.is_overseas,
        is_new_merchant=req.is_new_merchant,
        transaction_time=req.transaction_time,
    )
    risk = predict_risk(features)
    risk, decision = apply_rules(req.amount, risk)
    return {
        "risk_score": round(risk, 4),
        "decision": decision,
    }
