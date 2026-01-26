import pandas as pd
import yfinance as yf
import datetime as dt
from functools import lru_cache
from .data_processing import data_process

@lru_cache(maxsize=256)
def _download_yf(ticker: str, start_date: str, end_date: str):
    # auto_adjust=True makes Close adjusted for splits/dividends
    return yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)

def load_price_data(ticker: str, start_date: str, end_date: str | None = None):
    if end_date == "" or end_date is None:
        end_date = dt.date.today().strftime("%Y-%m-%d")

    try:
        df = _download_yf(ticker, start_date, end_date)
    except Exception as e:
        raise RuntimeError(f"Yahoo Finance download failed for {ticker}: {e}") from e

    if df is None or df.empty:
        return pd.DataFrame()

    # If multiindex columns appear, drop the extra level
    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(1, axis=1)

    # Ensure we have Close
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
            if df is None or df.empty:
                continue
            df = df.reset_index().rename(columns={"index": "Date"})
            df = df[["Date", "Close"]].rename(columns={"Close": ticker})
            dfs.append(df)
        except Exception as e:
            print(f"Error loading data for {ticker}: {e}")
            continue

    if not dfs:
        return None

    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on="Date", how="outer")

    merged_df = merged_df.sort_values("Date")

    price_cols = [c for c in merged_df.columns if c != "Date"]
    merged_df[price_cols] = merged_df[price_cols].ffill()

    merged_df["Portfolio"] = merged_df[price_cols].mean(axis=1)
    return merged_df

