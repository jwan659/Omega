import Auxilliary as aux
import datetime as dt
import Screen as Screen
import Indicators as i

# use constructors

def rsi(stock,data,date):
    if Screen.weekly_macd_screen(data.loc[:,'Weekly MACD'],date) == 1 and Screen.daily_macd_screen(data.loc[:,'Daily MACD'],date) == 1:
        if Screen.rsi_screen(data.loc[:,'RSI'],date,40) == 1 and Screen.multi_week_low_screen(data,date,15): # daily screen
            return 1
    elif Screen.weekly_macd_screen(data.loc[:,'Weekly MACD'],date) == -1:
        if Screen.rsi_screen(data.loc[:,'RSI'],date,70) == -1 and Screen.multi_week_high_screen(data,date,15): # daily screen
            return -1
    return 0

def impulse(stock,data,date):
    if Screen.weekly_macd_screen(data.loc[:,'Weekly MACD'],date) == 1 and Screen.daily_ema_screen(data.loc[:,'Daily EMA'],date):
        if Screen.force_screen(data.loc[:,'Force Index'],date):#if Screen.rsi_screen(data.loc[:,'RSI'],date,35) == 1:
            if Screen.multi_week_low_screen(data,date,15): # daily screen
                return 1
    elif Screen.weekly_macd_screen(data.loc[:,'Weekly MACD'],date) == -1 and not Screen.daily_ema_screen(data.loc[:,'Fast EMA'],date): # weekly screen
        if not Screen.force_screen(data.loc[:,'Force Index'],date) and Screen.multi_week_high_screen(data,date,15): # daily screen
            return -1
    return 0

def strat1(stock,data,date):
    if Screen.weekly_macd_screen(data.loc[:,'Weekly MACD'],date) == 1:# and Screen.force_screen(data.loc[:,'Force Index'],date):
        if Screen.multi_week_low_screen(data,date,15): # daily screen
            return 1
    return 0

def strat2(stock,data,date):
    if Screen.strong_weekly_macd_screen(data.loc[:,'Weekly MACD'],date) == 1 and Screen.daily_macd_screen(data.loc[:,'Daily MACD'],date) == 1:
        if Screen.daily_ema_screen(data.loc[:,'Daily EMA'],date) and Screen.force_screen(data.loc[:,'Force Index'],date):
            if Screen.multi_week_low_screen(data,date,15): # daily screen
                return 1
    return 0

def strat3(stock,data,date):
    if Screen.weekly_macd_screen(data.loc[:,'Weekly MACD'],date) == 1 and Screen.weekly_ema_screen(data.loc[:,'Weekly EMA'],date) == 1:
        if Screen.daily_macd_screen(data.loc[:,'Daily MACD'],date) == 1 and Screen.rsi_screen(data.loc[:,'RSI'],date,50) == 1:
            if Screen.multi_week_low_screen(data,date,15): # daily screen
                return 1
    return 0