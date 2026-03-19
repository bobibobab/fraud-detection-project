import numpy as np
from datetime import datetime

def build_feature_vector(amount: float, merchant_category: str,
                         is_overseas: bool, is_new_merchant: bool,
                         transaction_time: str) -> list:
    """
    Convert user payment input into a 30-dim feature vector [Time, V1~V28, Amount].
    V1~V28 are simulated based on input signals, mimicking PCA-transformed card features.
    """

    # Time: seconds elapsed since midnight
    try:
        t = datetime.strptime(transaction_time, "%H:%M")
        time_seconds = t.hour * 3600 + t.minute * 60
    except Exception:
        time_seconds = 0

    # Encode merchant category as an integer
    category_map = {
        "food": 0,
        "shopping": 1,
        "travel": 2,
        "entertainment": 3,
        "medical": 4,
        "other": 5,
    }
    cat_code = category_map.get(merchant_category, 5)

    # Simulate V1~V28 using input-based patterns (no actual PCA)
    rng = np.random.default_rng(seed=int(amount * 100) % 99991)
    base = rng.standard_normal(28)

    # V1: more negative for overseas transactions
    base[0] += -3.0 if is_overseas else 0.5

    # V2: more negative for new/unknown merchants
    base[1] += -2.0 if is_new_merchant else 0.3

    # V3: more negative for late-night transactions (22:00 ~ 06:00)
    hour = int(transaction_time.split(":")[0]) if ":" in transaction_time else 12
    base[2] += -2.5 if (hour >= 22 or hour <= 6) else 0.2

    # V4: higher for large transaction amounts
    base[3] += np.log1p(amount) * 0.3

    # V5~V7: influenced by merchant category
    base[4] += (cat_code - 2.5) * 0.4
    base[5] += -1.5 if merchant_category == "travel" and is_overseas else 0.1
    base[6] += 1.0 if merchant_category in ["food", "medical"] else -0.3

    # V10, V12, V14: combined fraud signal (overseas + high amount + new merchant)
    fraud_signal = (1 if is_overseas else 0) + (1 if is_new_merchant else 0) + (1 if amount > 1000 else 0)
    base[9]  += -fraud_signal * 1.5
    base[11] += -fraud_signal * 1.8
    base[13] += -fraud_signal * 2.0

    v_values = base.tolist()

    # Return full feature vector: [Time, V1~V28, Amount]
    return [time_seconds] + v_values + [amount]
