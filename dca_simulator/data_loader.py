import pandas as pd
import yfinance as yf
import datetime as dt
from .data_processing import data_process

def load_price_data(ticker: str, start_date: str, end_date: str | None = None):
    if end_date == "" or end_date is None:
        end_date = dt.date.today().strftime("%Y-%m-%d")

    df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)

    if df is None or df.empty:
        return pd.DataFrame()

    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(1, axis=1)

    if "Close" not in df.columns:
        return pd.DataFrame()

    df = df[["Close"]]
    df = data_process(df)
    return df

def load_multiple_price_data(tickers: list[str], start_date: str, end_date: str | None = None):
    dfs = []

    for ticker in tickers:
        try:
            df = load_price_data(ticker, start_date, end_date)
            if df.empty:
                continue

            df = df.reset_index()
            if "Date" not in df.columns:
                df = df.rename(columns={df.columns[0]: "Date"})

            df = df[["Date", "Close"]].rename(columns={"Close": ticker})
            dfs.append(df)

        except Exception as e:
            print(f"Error loading data for {ticker}: {e}")

    if not dfs:
        return None

    merged_df = dfs[0]
    for d in dfs[1:]:
        merged_df = pd.merge(merged_df, d, on="Date", how="outer")

    merged_df = merged_df.sort_values("Date")
    price_cols = [c for c in merged_df.columns if c != "Date"]
    merged_df[price_cols] = merged_df[price_cols].ffill()

    merged_df["Portfolio"] = merged_df[price_cols].mean(axis=1)
    return merged_df
    
