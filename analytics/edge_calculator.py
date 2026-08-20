import csv
import os
from core.storage_engine import DB_PATH, PROJECT_ROOT

def calculate_edge(target_setup: str) -> tuple:
    """
    Calculates the edge for a given trading setup based on historical data.
    
    Parameters:
        target_setup (str): The name of the trading setup to analyze."""

    setup_history = []

    # Check if the CSV file exists
    if not os.path.exists(DB_PATH):
       return (0.0, 0.0)  # Return zero edge if the file doesn't exist
    
    
    with open(DB_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['setup_id'] == target_setup and row['trade_outcome'] in ['Win', 'Loss']:
                setup_history.append(row)
               
    
    if len(setup_history) == 0:
        return (0.0, 0.0)  # Return zero edge if no trades found for the setup

    win_rate = sum(1 for trade in setup_history if trade['trade_outcome'] == 'Win') / len(setup_history) * 100
    recent_100 = setup_history[-100:]  # Get the last 100 trades for the setup
    t100_total = len(recent_100)
    t100_wins = sum(1 for trade in recent_100 if trade['trade_outcome'] == 'Win')
    t100_win_rate = (t100_wins / t100_total) * 100 if t100_total > 0 else 0
    return (round(win_rate, 2), round(t100_win_rate, 2))
    