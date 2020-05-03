import Auxilliary as aux
import Stop as s
import cython
from pandas.tseries.offsets import BDay

class Order():
    def __init__(self,symbol,entry,orderType,df,date,stop=0,target=0):
        self.symbol = symbol
        self.entry = entry
        self.orderType = orderType
        self.stop = stop
        self.entry = entry
        self.date = date
        self.rsi = df.loc[aux.date_to_string(date),'RSI']
        self.dEMA = df.loc[aux.date_to_string(date),'Daily EMA'] - df.loc[aux.date_to_string(date-BDay(1)),'Daily EMA']
        self.dMACD = df.loc[aux.date_to_string(date),'Daily MACD'] - df.loc[aux.date_to_string(date-BDay(1)),'Daily MACD']
    def setLong(self,df,marketValue,date):
        self.stop = s.nick_long_stop(df,date,15)
        self.target = 2*(self.entry-self.stop) + self.entry
        self.shares = calculate_shares(self.entry,self.stop,marketValue)
    def setShort(self,df,marketValue,date):
        self.stop = s.nick_short_stop(df,date,15)
        self.target = self.entry - 2*(self.stop-self.entry)
        self.shares = int((marketValue/100)/(self.stop-self.entry))

def calculate_shares(entry,stop,marketValue):
    shares = int((marketValue//(marketValue*0.01))/(entry-stop))
    while shares * entry > 0.2 * marketValue:
        shares -= 1
    return shares

def get_dEMA(order):
    return order.dEMA

def get_rsi(order):
    return order.rsi

def get_dMACD(order):
    return order.dMACD