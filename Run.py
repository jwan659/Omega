import Auxilliary as a
import Order as o
import Portfolio as p
import Strategy as s
import pandas as pd
from itertools import product
from multiprocessing import Pool
from yahoo_fin import stock_info as si
import os
import time

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

def run_helper(data,opportunities,orders,portfolio,type,date):
    i = 0
    print(orders.index)
    for stock in data:
        i += 1
        try:
            df = data[stock]
            df = df.set_index('Date')
            if stock not in orders.index: #if the stock has been ordered
                orderType = s.strat1(stock,df,date)
                if orderType == 1:
                    entry = si.get_live_price(stock)
                    opportunities = p.add_order(opportunities,stock,df,entry,orderType,portfolio,date)
        except:
            pass
    print(i)

def rank_orders(opportunities,method):

    if method =='RSI':
        opportunities.sort(key=o.get_rsi)
    elif method == 'EMA':
        opportunities.sort(key=o.get_dEMA,reverse=True)
    elif method == 'MACD':
        opportunities.sort(key=o.get_dMACD,reverse=True)

def run(data,portfolio,ordersFile,dict,type,date):
    
    opportunities = []
    orders = pd.read_csv(ordersFile,index_col="Stock")
    
    run_helper(data,opportunities,orders,portfolio,type,date)

    if len(opportunities) == 0:
        print('NO TRADING OPPORUNTIES IDENTIFIED')
    else: 
        print("Opportunities on {}".format(date))
        rank_orders(opportunities,'MACD')

        for order in opportunities:
            print(order.symbol,order.dEMA,order.rsi,order.dMACD)

    orders = p.place_orders(portfolio,orders,opportunities,date)
    orders.to_csv(ordersFile)

    return portfolio