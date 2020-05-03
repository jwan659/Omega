import Auxilliary as aux

def nick_long_stop(df,date,lookback):
    d = aux.find_prev_date(df,date)
    low1 = min(df.loc[aux.date_to_string(date),"Low"],df.loc[aux.date_to_string(d),"Low"])
    low2 = max(df.loc[aux.date_to_string(date),"Low"],df.loc[aux.date_to_string(d),"Low"])
    for i in range(2,lookback):
        d = aux.find_prev_date(df,d)
        if df.loc[aux.date_to_string(d),"Low"]<low1: 
            low2 = low1
            low1 = df.loc[aux.date_to_string(d),"Low"]
        elif df.loc[aux.date_to_string(d),"Low"]<low2: 
            low2 = df.loc[aux.date_to_string(d),"Low"]
    return low2

def nick_short_stop(df,date,lookback):
    d = aux.find_prev_date(df,date)
    high1 = max(df.loc[aux.date_to_string(date),"High"],df.loc[aux.date_to_string(d),"High"])
    high2 = min(df.loc[aux.date_to_string(date),"High"],df.loc[aux.date_to_string(d),"High"])
    for i in range(2,lookback):
        d = aux.find_prev_date(df,d)
        if df.loc[aux.date_to_string(d),"High"]>high1: 
            high2 = high1
            high1 = df.loc[aux.date_to_string(d),"High"]
        elif df.loc[aux.date_to_string(d),"High"]>high2: 
            high2 = df.loc[aux.date_to_string(d),"High"]
    return high2