import Auxilliary as a
import Data as Data
import Run as r
import datetime as dt
import pandas as pd
import os
from datetime import datetime

if __name__=="__main__":
    initial_investment = 200000.0
    start = datetime(2013,1,1)
    date = dt.datetime.today
    portfolio = {"Marketvalue":initial_investment,"Equity":0,"Cash":initial_investment}
    a.initialize_orders_csv("BOrders.csv")
    
    # Data Shit
    data = []
    if os.path.isdir('Data') is False:
        Data.get_data_from_yahoo()
        
        print("Hello")
    os.mkdir('/Data1') 
    #Update data instead
    
        # for item in Data folder, update most recent data
    currDate = start
    dict = {"Targets":0,"Stops":0}
    print("STARTING BACKTEST")
    #strategy must be defined here
    while currDate != dt.datetime.today:
        count = 0 
        # testData = Fit.rolling_window(data, count)

        # fit data to find best strategy

        # test strategy on following year data

        portfolio = r.run(data,portfolio,'BOrders.csv',dict,0,date)
        date = a.next_business_day(date)
        print("\n")

    print("Target rate of {} made on {} trades".format(dict["Targets"]/(dict["Stops"]+dict["Targets"]),dict["Stops"]+dict["Targets"]))
    print(portfolio)
    