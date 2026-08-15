import csv
import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'trading_log.csv')

def sanitize_text(text_input) -> str:
    """
    Sanitizes the input text by removing any commas, semicolons and newline insertions.
    """
    
    sanitized_text = text_input.strip().replace(',', ' ').replace(':', ' ').replace('\n', ' ')
    return sanitized_text

def append_trade(trade_data_list):
    """
    Appends a new trade entry to the trading log CSV file.
    
    Parameters:
        trade_data_list (list): A list containing trade data in the following order:
            [trade_id, asset, Set-up ID, HTF Bias, LTF Bias, Risk, Postion size, Entry Price, Stop Loss, Take Profit, MAE, MFE, Exit-Trigger, Trade Outcome, friction_Log]
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Append the trade data to the CSV file
    with open(DB_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
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
            if row['Trade Outcome'] == 'Open':
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
                row['Exit-Trigger'] = exit_trigger
                row['Trade Outcome'] = trade_outcome
                row['MAE'] = mae
                row['MFE'] = mfe
                row['friction_Log'] = sanitize_text(friction_log)
            all_rows.append(row)
    
    # Write the updated rows back to the CSV file
    with open(DB_PATH, mode='w', newline='') as file:
        fieldnames = ['trade_id', 'asset', 'Set-up ID', 'HTF Bias', 'LTF Bias', 'Risk', 'Postion size', 
                      'Entry Price', 'Stop Loss', 'Take Profit', 'MAE', 'MFE', 
                      'Exit-Trigger', 'Trade Outcome', 'friction_Log']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)