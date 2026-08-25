import csv
import os
from core.storage_engine import DB_PATH
import re
from collections import Counter

STOP_WORDS = {
    'i', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'so', 'had', 'out', 'was', 'my', 'it'
}

def audit_execution(target_setup: str) -> tuple:
    """
    Audits the execution of trades for a specific setup. And ejects a tuple containing two floats average MAE and average MFE for the target setup.

    Parameters:
        target_setup (str): The setup ID to audit.
    Returns:
        tuple: A tuple containing the average MAE and average MFE for the target setup and the top friction triggers.
        """
    mae_list = []
    mfe_list = []   
    all_friction_words = []
    if not os.path.exists(DB_PATH):
        return (0.0, 0.0, [])  # Return zeros if the file doesn't exist
    with open(DB_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['setup_id'] == target_setup and row['trade_outcome'] != 'Open':
                mae_list.append(float(row['mae']))
                mfe_list.append(float(row['mfe']))
                # Collect friction words from the trade description
                log_text = row.get('friction_log', '')
                words = re.findall(r'\b\w+\b', log_text.lower())
                all_friction_words.extend(words)
    if len(mae_list) == 0 or len(mfe_list) == 0:
        return (0.0, 0.0, [])  # Return zeros if there are no closed trades for the target setup
    average_mae = sum(mae_list) / len(mae_list)
    average_mfe = sum(mfe_list) / len(mfe_list)
    meaningful_words = [word for word in all_friction_words if word not in STOP_WORDS]
    top_triggers = Counter(meaningful_words).most_common(5)
    return (round(average_mae, 2), round(average_mfe, 2), top_triggers)