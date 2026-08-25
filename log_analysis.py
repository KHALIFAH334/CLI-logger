from datetime import datetime
from core.storage_engine import append_analysis

analysis_type = input("Enter the analysis type (e.g., 'Daily', 'Weekly', 'Monthly'): ")
market_regime = input("Enter the market regime (e.g., 'Bullish', 'Bearish', 'Sideways'): ")
bias = input("Enter the bias (e.g., 'Bull', 'Bear'): ")
key_levels = input("Enter the key levels: ")
notes = input("Enter any additional notes: ")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
analysis_row = [timestamp, analysis_type, market_regime, bias, key_levels, notes]
append_analysis(analysis_row)
print("Analysis entry has been appended to the daily analytics CSV file.")