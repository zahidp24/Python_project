import pandas as pd

def price_data_prep(df: pd.DataFrame):
    """Make sure the data is in a clean format + index is correct"""
    df = df.copy()

    if isinstance(df.index, pd.MultiIndex):
        df = df.droplevel(0) #because yfinance data is multi indexed

    df.index = pd.to_datetime(df.index) #just in case
    df = df.sort_index()

    df = df[["Close"]]

    df = df.dropna()
    
    return df