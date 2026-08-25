from analytics.edge_calculator import calculate_edge

def evaluate_grade(setup_id: str, htf_bias: str, ltf_bias: str) -> str:
    """
    Evaluates the grade of a trading setup based on its win rate and T 100 trades win rate.

    Parameters:
        setup_id (str): The unique identifier of the trading setup.
        htf_bias (str): The higher time frame bias for the trade.
        ltf_bias (str): The lower time frame bias for the trade.  
    """
    score = 0
    if htf_bias.lower() == ltf_bias.lower():
        score += 50 #Perfect alignment of biases
    else:
        score += 0 #Fighting the macro trend
    all_time_wr, t100_wr = calculate_edge(setup_id)
    if all_time_wr == 0.0:
        score += 30 #Neutral baseline for new setup with no data
    elif all_time_wr >= 50:
        score += 50 #High all-time win rate
    elif all_time_wr >= 40:
        score += 25 #Moderate all-time win rate
    elif all_time_wr < 40:
        score += 0 #Low all-time win rate
    

    if score == 100:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C" 
    elif score <= 50:
        return "F"
        
