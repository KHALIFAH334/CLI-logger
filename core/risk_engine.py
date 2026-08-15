MAX_RISK = 0.005

def calculate_sizing(account_balance: float, entry_price: float, stop_loss: float) -> float:
    risk_per_trade = account_balance * MAX_RISK
    price_distance = abs(entry_price - stop_loss)
    
    if price_distance == 0:
        raise ValueError("Entry price and stop loss cannot be the same.")
    
    position_size = risk_per_trade / price_distance
    lot = position_size/100000
    return (round(lot, 2))