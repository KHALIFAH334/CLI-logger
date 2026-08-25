import csv
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'trading_log.csv')
ANALYSIS_DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'daily_analytics.csv')

def sanitize_text(text_input) -> str:
    """
    Sanitizes the input text by removing any commas, semicolons and newline insertions.
    """
    
    sanitized_text = text_input.strip().replace(',', ' ').replace(':', ' ').replace('\n', ' ')
    return sanitized_text

FIELDNAMES = ['trade_id', 'timestamp', 'asset', 'direction', 'setup_id', 'htf_bias', 'ltf_bias', 'risk', 'position_size',
              'entry_price', 'stop_loss', 'take_profit', 'mae', 'mfe',
              'exit_trigger', 'trade_outcome', 'friction_log']

def append_trade(trade_data_list):
    """
    Appends a new trade entry to the trading log CSV file.
    
    Parameters:
        trade_data_list (list): A list containing trade data in the following order:
            [trade_id, timestamp, asset, direction, setup_id, htf_bias, ltf_bias, Risk, position_size, entry_price, stop_loss, take_profit, MAE, MFE, exit_trigger, trade_outcome, friction_Log]
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    file_exists = os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0
    
    # Append the trade data to the CSV file
    with open(DB_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(FIELDNAMES)
        writer.writerow(trade_data_list)

def get_open_trades():
    """
    Retrieves all open trades from the trading log CSV file.
    
    Returns:
        list: A list of dictionaries, each representing an open trade.
    """
    open_trades = []
    
    # Check if the CSV file exists
    if not os.path.exists(DB_PATH):
        return open_trades  # Return an empty list if the file doesn't exist
    
    with open(DB_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['trade_outcome'] == 'Open':
                open_trades.append(row)
    
    return open_trades
def close_trade(trade_id, exit_trigger, trade_outcome, mae, mfe, friction_log):
    """
    Closes a trade by updating its details in the trading log CSV file.
    
    Parameters:
        trade_id (str): The unique identifier of the trade to be closed.
        exit_trigger (str): The trigger that caused the trade to close.
        trade_outcome (str): The outcome of the trade (e.g., 'Win', 'Loss').
        mae (float): Maximum Adverse Excursion for the trade.
        mfe (float): Maximum Favorable Excursion for the trade.
        friction_log (str): A log of any friction encountered during the trade.
    """
    # Check if the CSV file exists
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Trading log file does not exist.")
    
    all_rows = []
    with open(DB_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['trade_id'] == trade_id:
                row['exit_trigger'] = exit_trigger
                row['trade_outcome'] = trade_outcome
                row['mae'] = mae
                row['mfe'] = mfe
                row['friction_log'] = sanitize_text(friction_log)
            all_rows.append(row)
    
    # Write the updated rows back to the CSV file
    with open(DB_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(all_rows)

def initialize_analysis_db():
    """
    Initializes the daily analytics CSV file with headers if it doesn't already exist.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(ANALYSIS_DB_PATH), exist_ok=True)
    
    if not os.path.exists(ANALYSIS_DB_PATH):
        with open(ANALYSIS_DB_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'analysis_type', 'market_regime', 'bias', 'key_levels', 'notes'])

def append_analysis(analysis_data: list):
    os.makedirs(os.path.dirname(ANALYSIS_DB_PATH), exist_ok=True)
    with open(ANALYSIS_DB_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(analysis_data)

if __name__ == "__main__":
    print("Initiating storage engine unit test...")
    test_trade_data = ["test_uuid_1234", "2026-08-16 07:00:00", "EURUSD", "Long", 
        "Setup_A", "Bull", "Bull", 0.005, 1.25, 
        1.1000, 1.0900, 1.1200, 
        0.0, 0.0, "", "Open", ""]
    append_trade(test_trade_data)
    initialize_analysis_db()
    print("Test complete. Check the trading_log.csv file in the data directory for the appended test trade.")