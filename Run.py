import Auxilliary as a
import Order as o
import Strategy as s
import pandas as pd
from itertools import product
from multiprocessing import Pool
from yahoo_fin import stock_info as si
import os
import time
import json
import Data
import concurrent.futures

def update_marketvalue(portfolio,orders):
    portfolio["Equity"] =(orders['Entry']*orders['Shares']).sum()
    portfolio["Marketvalue"] = portfolio["Cash"] + portfolio["Equity"]
    return portfolio

def get_price(type,stock,df,date):
    if type == 0:
        price = (df.loc[a.date_to_string(date),"High"]+df.loc[a.date_to_string(date),"Low"])/2
    elif type == 1:
        print(stock)
        price = si.get_live_price(stock)
    return price
   
def rank_orders(orders,method):
    if method =='RSI':
        orders.sort(key=lambda x: x.rsi)
    elif method == 'EMA':
        orders.sort(key=lambda x: x.dEMA,reverse=True)
    elif method == 'MACD':
        orders.sort(key=lambda x: x.dMACD, reverse=True)

def scan(account, type, date):
    
    data = Data.get_stock_list()
    print(data)
    orders = []
    totalEquity = (account.balances['combinedBalances'][1]['totalEquity'])
    
    #remove bought stocks
    print("Checking for stocks already bought")
    for currPos in account.positions['positions']:
        for stock in data:
            if currPos == stock:
                print(currPos + 'has been bought')
                data.remove(stock)
    # stock hasn't been bought and could be traded
    for stock in data:
        df = pd.read_csv('Data/'+stock+'.csv',index_col='Date')
        try:
            buy = s.strat2(stock,df,date)
            if buy:
                currPrice = si.get_live_price(stock)
                newOrder = o.Order(stock,currPrice,df,date)
                newOrder.setLong(df, totalEquity, date)
                orders.append(newOrder) 
        except:
            print('Error Getting Stock Prices')
            pass

    if len(orders) == 0:
        print('Hold portfolio')
    else: 
        print("Opportunities on {}".format(date))
        rank_orders(orders,'MACD')
        for order in orders:
            print(order.symbol,order.dEMA,order.rsi,order.dMACD)
