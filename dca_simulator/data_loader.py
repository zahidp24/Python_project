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




def load_multiple_price_data(tickers: list[str], start_date: str, end_date: str | None = None):
    """Download price data for multiple tickers and return a single DataFrame used for equal-weight portfolio"""

    dfs = []

    for ticker in tickers:
        try:
            df = load_price_data(ticker, start_date, end_date)
            if df is None or df.empty:
                continue
            df = df.reset_index().rename(columns={"index": "Date"})
            df = df[["Date", "Close"]].rename(columns={"Close": ticker}) #load_price_data() returns the date as the index but there is no "Date" column to select (line 38 & 39).
            dfs.append(df)
        except Exception as e:
            print(f"Error loading data for {ticker}: {e}")
            continue

    if not dfs:
        return None
    
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on="Date", how="inner")

    price_cols = [c for c in merged_df.columns if c != "Date"]
    merged_df["Portfolio"] = merged_df[price_cols].mean(axis=1) #If one ticker fails to download, you continue, so that ticker’s column ticker’s column won’t exist. 
    #but you still try to compute mean over  full original list. (line 52 & 53)
    return merged_df
