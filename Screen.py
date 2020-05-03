import Auxilliary as aux
import datetime as dt
import Indicators as i
from pandas.tseries.offsets import BDay

def strong_weekly_macd_screen(macd,date):
    date = date - dt.timedelta(days=date.weekday()) # convert to Monday
    d = date - dt.timedelta(days=7)
    if macd.loc[aux.date_to_string(d)]<macd.loc[aux.date_to_string(date)] and macd.loc[aux.date_to_string(date)]<0:
        return 1
    elif macd.loc[aux.date_to_string(d)]>macd.loc[aux.date_to_string(date)] and macd.loc[aux.date_to_string(date)]>0:
        return -1
    return 0

def weekly_macd_screen(macd,date):
    date = date - dt.timedelta(days=date.weekday())
    d = date - dt.timedelta(days=7)
    if macd.loc[aux.date_to_string(d)]<macd.loc[aux.date_to_string(date)]:
        return 1
    elif macd.loc[aux.date_to_string(d)]>macd.loc[aux.date_to_string(date)] and macd.loc[aux.date_to_string(date)]>0:
        return -1
    return 0

def strong_daily_macd_screen(macd,date):
    d = date - BDay(1)
    if macd.loc[aux.date_to_string(d)]<macd.loc[aux.date_to_string(date)] and macd.loc[aux.date_to_string(date)]<0:
        return 1
    elif macd.loc[aux.date_to_string(d)]>macd.loc[aux.date_to_string(date)]:
        return -1
    return 0

def daily_macd_screen(macd,date):
    d = date - BDay(1)
    if macd.loc[aux.date_to_string(d)]<macd.loc[aux.date_to_string(date)]:
        return 1
    elif macd.loc[aux.date_to_string(d)]>macd.loc[aux.date_to_string(date)]:
        return -1
    return 0

def alt_daily_macd_screen(macd,date):
    d = date - BDay(1)
    if macd.loc[aux.date_to_string(date)]<0:
        return 1
    elif macd.loc[aux.date_to_string(d)]>macd.loc[aux.date_to_string(date)]:
        return -1
    return 0

def weekly_ema_screen(ema,date):
    date = date - dt.timedelta(days=date.weekday())
    d = date - dt.timedelta(days=7)
    if ema.loc[aux.date_to_string(date)]>ema.loc[aux.date_to_string(d)]:
        return 1
    return -1

def force_screen(force,date):
    if force.loc[aux.date_to_string(date)]<0:
        return True
    return False

def daily_ema_screen(ema,date):
    d = date - BDay(1)
    if ema.loc[aux.date_to_string(date)]>ema.loc[aux.date_to_string(d)]:
        return True
    return False

def impulse_macd(df,n):
    df_macd = i.macd_hist(df)
    if df_macd.iloc[-n]>df_macd.iloc[-n-1]:
        return True
    return False

def impulse_screen(df,n):
    weekly = aux.to_weekly(df)
    if daily_ema_screen(weekly,n) and impulse_macd(weekly,n):
        if (daily_ema_screen(df,n) and impulse_macd(df,n)):
            return 1
    elif not(daily_ema_screen(weekly,n) or impulse_macd(weekly,n)):
        if not(daily_ema_screen(df,n) or impulse_macd(df,n)):
            return -1
    return 0

def rsi_screen(df,date,n):
    if df.loc[aux.date_to_string(date)]<n:
        return 1
    elif df.loc[aux.date_to_string(date)]>n:
        return -1
    return 0

def multi_week_low_screen(df,date,lookback):
    if df.loc[aux.date_to_string(date),'Low'] != df.loc[aux.date_to_string(
        date-dt.timedelta(days=lookback)):aux.date_to_string(date),'Low'].min():
        return True
    return False

def multi_week_high_screen(df,date,lookback):
    if df.loc[aux.date_to_string(date),'High'] != df.loc[aux.date_to_string(
        date-dt.timedelta(days=lookback)):aux.date_to_string(date),'High'].max():
        return True
    return False