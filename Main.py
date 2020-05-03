import Data as Data
import Run as r
import Portfolio
import Strategy
import csv
import datetime as dt
import time
import os
import pandas as pd

if __name__ == '__main__':

    # 1. Read in existing accounting information
    portfolio = {}
    with open('Portfolio.csv', mode='r') as infile:
        reader = csv.reader(infile)
        portfolio = {rows[0]:float(rows[1]) for rows in reader}
        print(portfolio)

    # 2. Retrieve stock data from yahoo finance
    stock_data = Data.get_raw_data()
    
    valid_data = Data.aggregrate_data(stock_data)
    dict = {"Targets":0,"Stops":0}

    # 3. Find trading opportunities and put them in the Orders csv file
    print('FINDING OPPORTUNITIES')
    portfolio = r.run(valid_data,portfolio,'Orders.csv',dict,1,dt.datetime.today())

    # 4. Readjust portfolio information based on new trades etc.
    w = csv.writer(open('Portfolio.csv', "w"))
    for key, val in portfolio.items():
        w.writerow([key,val])

    print("END PROGRAM")
   
    
    

