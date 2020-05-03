import Auxilliary as aux
import datetime as dt
import pandas as pd
import Order as o
import Stop as s
from pandas.tseries.offsets import BDay

# add a long or short order
def add_order(opportunities,stock,df,entry,orderType,portfolio,date):
    newOrder = o.Order(stock,entry,orderType,df,date)
    if orderType == 1:
        newOrder.setLong(df,portfolio["Marketvalue"],date)
    else:
        newOrder.setShort(df,portfolio["Marketvalue"],date)
    
    if newOrder.dMACD > 0.1: #and if 5 < newOrder.shares <= 40:
        opportunities.append(newOrder)
    return opportunities
    
# Return true if long order has hit stop
def place_orders(portfolio,orders,opportunities,date):
    if opportunities:
        count = 0
        for order in opportunities:
            if order.shares * order.entry < portfolio["Cash"]:
                s = pd.Series([order.entry,order.stop,order.target,order.shares,order.orderType,order.date],index=orders.columns)
                s.name = order.symbol
                orders = orders.append(s)
                portfolio["Cash"] = portfolio["Cash"] - round(order.shares * order.entry,2)
                portfolio["Equity"] = portfolio["Equity"] + round(order.shares * order.entry,2)
                print("Long {} shares of {} at {} with stop at {} and target at {} on {}".format(
                    order.shares,order.symbol,round(order.entry,2),round(order.stop,2),round(order.target,2),date))
                count = count + 1
    return orders

def exit_long(stock,order,currPrice,date):
    if currPrice > order.loc["Target"]:
        print ("Sell {} at target {} on {}.".format(stock,round(order.loc["Target"],2),date))
        return 1
    elif currPrice < order.loc["Stop"]:
        print ("Sell {} at stop {} on {}".format(stock,round(order.loc["Stop"],2),date))
        return -1
    return 0

# Return true if short order has hit stop
def exit_short(stock,order,currPrice,date):
    if currPrice < order.loc["Target"]:
        print ("Sell {} at {} on {}.".format(stock,round(order.loc["Target"],2),date))
        return 1
    elif currPrice > order.loc["Stop"]:
        print ("Sell {} at {} on {}".format(stock,round(order.loc["Stop"],2),date))
        return -1
    return 0
# Calculate ROI and add back to value
def exit_market(stock,order,val,portfolio,dict) :
    #if the order type is long
    if order.loc["Order Type"] == 1:
        if val == 1:
            dict["Targets"] = dict["Targets"] + 1
            portfolio["Cash"] = round(portfolio["Cash"] + order.loc["Shares"]*order.loc["Target"],2)
        else:
            dict["Stops"] = dict["Stops"] + 1
            portfolio["Cash"] = round(portfolio["Cash"] + order.loc["Shares"]*order.loc["Stop"],2)
    elif order.loc["Order Type"] == -1:
        if val == 1:
            portfolio["Cash"] = round(portfolio["Cash"] + order.loc["Shares"]*(2*order.loc["Entry"]-order.loc["Target"]),2)
        else:
            portfolio["Cash"] = round(portfolio["Cash"] + order.loc["Shares"]*(2*order.loc["Entry"]-order.loc["Stop"]),2)
    return