def apply_rules(amount, risk):
    if amount > 2000:
        risk += 0.1
    
    if amount > 5000:
        risk += 0.1

    if risk > 1:
        risk = 1

    if risk > 0.5:
        decision = "reject"
    
    else:
        decision = "approve"
    
    return risk, decision