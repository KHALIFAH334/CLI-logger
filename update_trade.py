import sys
from core.storage_engine import get_open_trades, close_trade
active_trades = get_open_trades()
if not active_trades:
    print("No open trades found.")
    sys.exit(0)
else:
    print("Open Trades:")
for index, trade in enumerate(active_trades):
    print(f"{index}. Trade ID: {trade['trade_id']}, Asset: {trade['asset']}, Direction: {trade['direction']}, Entry Price: {trade['entry_price']}")

interaction = int(input("Select the trade number to close: "))
selected_trade = active_trades[interaction]
trade_id = selected_trade['trade_id']
exit_trigger = input("Enter the exit trigger: ")
trade_outcome = input("Enter the trade outcome (Win/Loss): ")
mae = float(input("Enter the Maximum Adverse Excursion (MAE): "))
mfe = float(input("Enter the Maximum Favorable Excursion (MFE): "))
friction_log = input("Enter any friction log details: ")
close_trade(trade_id, exit_trigger, trade_outcome, mae, mfe, friction_log)
print(f"Trade {trade_id} has been closed and updated in the trading log.")