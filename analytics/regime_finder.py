HTF_Bias = input("What is the Trend? ")
mrkt_vol = input("How volatile is the market? ")
HTF_Bias = HTF_Bias.lower
LTF_Bias = input("What is the market saying on the lower time frame? ")
HTF-LTF-alignment = input("Is the High time frame aligned? ")
def range():
    if HTF_Bias == 'Range':
        D_c = int(input("How many candles has it been ranging for"))
        R-high = input("What is the range high?")
        R-low = input("What is the range low? ")
        Test_high = input("How many times did the market test the range high? ")
        Test_low = input("How many times did the market test the range low?")
        news = input("Was there any geopolitical news before after or during the trend?")
        print(f"The market has been ranging for {D_c} days, the range high is ")
        with open ('trading_log.csv', 'a') as f:
            f.write
def uptrend():
    if HTF_Bias == 'Up Trend':
        D_c = int(input("How many candles has it been trending for? "))
        