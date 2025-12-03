import pandas as pd
import yfinance as yf

def load_price_data(ticker: str, start_date: str, end_date: str):
    """Download daily adj. close prices for a stock""" 
        #yfinance does not have an 'Adj Close' column anymore 
    df = yf.download(ticker, start=start_date, end=end_date)

    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(1, axis=1) #drop Ticker
        

    df = df[["Close"]]
    return df #'Close' is already adjusted for div. and stock splits



