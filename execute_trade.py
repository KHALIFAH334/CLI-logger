import uuid
from datetime import datetime
from core.risk_engine import calculate_sizing
from core.storage_engine import append_trade
from core.risk_engine import MAX_RISK
from analytics.edge_calculator import calculate_edge
from setup_grade import evaluate_grade
import sys


asset = input("Enter the asset: ")
setup_id = input("Enter the Set-up ID: ")
direction = input("Enter the direction (Long/Short): ")
htf_bias = input("Enter the HTF Bias: ")
ltf_bias = input("Enter the LTF Bias: ")
setup_grade = evaluate_grade(setup_id, htf_bias, ltf_bias)
win_rate, t100_win_rate = calculate_edge(setup_id)
print(f"Set-up {setup_id} | All-Time: {win_rate}% | T 100 Trades: {t100_win_rate}%")
print(f"Setup Grade: {setup_grade}")
print("-" * 40)
if setup_grade == "F":
    print("Warning: This setup has a failing grade. Proceed with caution.")
    proceed = input("Do you want to continue? (yes/no): ")
    if proceed.lower() != "yes":
        print("Trade entry aborted. Good discipline")
        sys.exit(0)

account_balance = float(input("Enter your account balance: "))
entry_price = float(input("Enter the entry price: "))
stop_loss = float(input("Enter the stop loss: "))
take_profit = float(input("Enter the take profit: "))

Risk = account_balance * MAX_RISK

def directional_validation():
    if direction == "Long" and stop_loss >= entry_price:
        raise ValueError("For a Long trade, the stop loss must be below the entry price")
    elif direction == "Short" and stop_loss <= entry_price:
        raise ValueError("For a Short trade, the stop loss must be above the entry price")
directional_validation()
position_size = calculate_sizing(account_balance, entry_price, stop_loss)

trade_id = str(uuid.uuid4())
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
trade_outcome = "Open"
(MAE, MFE, exit_trigger, friction_log) = (0.0, 0.0, "", "")

trade_data_list = [
    trade_id,
    timestamp,
    asset,
    direction,
    setup_id,
    htf_bias,
    ltf_bias,
    Risk,
    position_size,
    entry_price,
    stop_loss,
    take_profit,
    MAE,
    MFE,
    exit_trigger,
    trade_outcome,
    friction_log
]

append_trade(trade_data_list)