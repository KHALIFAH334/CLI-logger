import datetime
#Collect the trade data
asset_traded = input("What pair are you trading today? ")
date = datetime.datetime.now()
HTF_Bias = input("what is the current trend? ")
setup_id = input("What set-up are you taking?")
#I taught of using past data to influence future decisions so this print section is going to show updated setup_winrate of that particualr setup and i know that we are going to have to use some conditionals and an if loop but lets leave it as it is for today
print(f"From past data this set-up has had a {setup_winrate} winrate")
session_id = input("What is the current trade session? ")
risk = 0.005
account_balance = int(input(" What is your account balance?"))
#THe postion size is going to be imported from the risk_engine.py as discussed before
position_size
entry = float(input("What is your entry price? "))
SL = float(input("What is your Stop loss? "))
TP = float(input("What is the Trade target? "))
risk_reward = (TP - entry)/(entry - SL)
risk_reward = abs(risk_reward)
