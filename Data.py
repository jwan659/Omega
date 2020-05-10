import Auxilliary as aux;   import bs4 as bs;   import datetime as dt
import Indicators as i;     import os;          import pandas as pd
import pickle;              import requests;    import concurrent.futures
from datetime import datetime
from yahoo_fin import stock_info as si
from pandas_datareader import data as web

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('table',{'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker.replace('.','-').strip())
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
    return tickers

def add_indicators(df):
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df['Weekly EMA'] = i.faster_ema(aux.to_weekly(df))
    df['Daily EMA'] = i.fast_ema(df)
    df['Weekly MACD'] = i.macd_hist(aux.to_weekly(df))
    df['Daily MACD'] = i.macd_hist(df)
    df['RSI'] = i.rsi(df)
    df['Force Index'] = i.force_index(df)
    return df

def get_stock_from_yahoo(ticker):
    print(ticker)
    try:
        df = web.DataReader(ticker, 'yahoo', start='2010-01-01', end=dt.datetime.today())
        df = pd.DataFrame(add_indicators(df))

        # check if there are more than thirty days of prices
        date = dt.datetime.today() - dt.timedelta(days=30)
        if pd.to_datetime(df.iloc[0,0]) + dt.timedelta(days=30) <= date:
            df.to_csv('Data/%s.csv' %ticker,index=True)
    except:
        print("Stock not found")
        pass

# Get data of snp500 stocks
def get_raw_data():
    tickers = save_sp500_tickers()
    print(dt.datetime.today())
    print(len(tickers))
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        [executor.submit(get_stock_from_yahoo, ticker) for ticker in tickers]
    print('Stocks have been stored')

def get_stock_list():
    data = []
    dir = os.fsencode('Data')
    for stock in os.listdir(dir):
        data.append(os.fsdecode(os.path.splitext(stock)[0]))
    return data