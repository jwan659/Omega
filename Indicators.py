import pandas as pd
import numpy as np
import numba
# Returns a MACD series
def macd_hist(df):
    exp1 = df['Close'].ewm(span=12,adjust=False).mean()
    exp2 = df['Close'].ewm(span=26,adjust=False).mean()
    temp = exp1-exp2
    signal = temp.ewm(span=9,adjust=False).mean()
    ret = pd.Series(temp-signal,name='MACD')
    return ret
# Returns a Force Index series
def force_index(df): 
    return pd.Series((df['Close'].diff(1)*df['Volume']).ewm(span=2,adjust=False).mean(),name='Force Index')
# Returns an RSI series
def rsi(df,n=14):
    deltas = (df['Close']-df['Close'].shift(1)).fillna(0)
    avg_of_gains = deltas[1:n+1][deltas > 0].sum() / n
    avg_of_losses = -deltas[1:n+1][deltas < 0].sum() / n
    rsi_series = pd.Series(0.0, deltas.index,name='RSI')
    up = lambda x: x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in deltas[n+1:]:
        avg_of_gains = ((avg_of_gains * (n-1)) + up(d)) / n
        avg_of_losses = ((avg_of_losses * (n-1)) + down(d)) / n
        if avg_of_losses != 0:
            rs = avg_of_gains / avg_of_losses
            rsi_series[i] = 100-(100/(1+rs))
        else:
            rsi_series[i] = 100
        i += 1
    return rsi_series
# Returns the fast ema

def faster_ema(df):
    return df['Close'].ewm(span=12,adjust=False).mean()

def fast_ema(df):
    return df['Close'].ewm(span=13,adjust=False).mean()

def slow_ema(df):
    return df['Close'].ewm(span=26,adjust=False).mean()