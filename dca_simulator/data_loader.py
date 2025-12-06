import pandas as pd
import yfinance as yf
import datetime as dt
from .data_processing import data_process  

def load_price_data(ticker: str, start_date: str, end_date: str | None = None):
    """Download daily adj. close prices for a stock""" 
        
    if end_date == "" or end_date is None:
        end_date = dt.date.today().strftime("%Y-%m-%d")  

    df = yf.download(ticker, start=start_date, end=end_date)

    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(1, axis=1) #drop Ticker
        

    df = df[["Close"]]#yfinance does not have an 'Adj Close' column anymore 
    #'Close' is already adjusted for div. and stock splits

    df = data_process(df)

    return df 



