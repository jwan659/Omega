import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import Indicators as i
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import USFederalHolidayCalendar
# Function to initialize an orders csv
def initialize_orders_csv(filename):
    if not os.path.isfile(filename):
        columns = ["Stock","Entry","Stop","Target","Shares","Order Type"]
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename,index=False)
    return
# Helper function to find the previous business date
def find_prev_date(df,date):
    done = False
    while not done:
        date = date - dt.timedelta(days=1)
        if date_to_string(date) in df.index:
            done = True
    return date
# Function to transform to weekly data
def to_weekly(df):
    logic = {'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}
    offset = pd.offsets.timedelta(days=-6)
    df = df.resample('W', loffset=offset).apply(logic)
    return df
# Function to convert a date object to string
def date_to_string(date):
    return date.strftime("%Y-%m-%d")
# Function to get the next business day
def next_business_day(date):
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays()
    date = date + BDay(1)
    date = date.to_pydatetime()
    while date in holidays: date = date + BDay(1); date = date.to_pydatetime()
    return date