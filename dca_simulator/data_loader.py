import pandas as pd
import yfinance as yf
import datetime as dt
from pathlib import Path
from .data_processing import data_process  

REPO_ROOT = Path(__file__).resolve().parent.parent
AAPL_CSV = REPO_ROOT / "AAPL_2000_2025.csv"

def load_price_data(ticker: str, start_date: str, end_date: str | None = None):
    """Load daily Close prices for a stock. Falls back to local CSV if yfinance fails/rate-limits."""
        
    if end_date == "" or end_date is None:
        end_date = dt.date.today().strftime("%Y-%m-%d")  

    ticker = ticker.upper().strip()

    # 1) Try yfinance
    try:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    except Exception:
        df = pd.DataFrame()

    # handle yfinance multiindex columns
    if isinstance(getattr(df, "columns", None), pd.MultiIndex):
        df = df.droplevel(1, axis=1)

    # 2) Fallback to local CSV (AAPL only)
    if (df is None or df.empty) and ticker == "AAPL" and AAPL_CSV.exists():
        raw = pd.read_csv(AAPL_CSV)

        # If there's a Date column, use it; otherwise assume first column is date
        if "Date" in raw.columns:
            raw["Date"] = pd.to_datetime(raw["Date"], errors="coerce")
            raw = raw.dropna(subset=["Date"]).set_index("Date")
        else:
            raw.iloc[:, 0] = pd.to_datetime(raw.iloc[:, 0], errors="coerce")
            raw = raw.dropna(subset=[raw.columns[0]]).set_index(raw.columns[0])

        raw = raw.sort_index()

        if "Close" in raw.columns:
            df = raw[["Close"]]
        elif "Adj Close" in raw.columns:
            df = raw[["Adj Close"]].rename(columns={"Adj Close": "Close"})
        else:
            df = pd.DataFrame()

        if not df.empty:
            df = df.loc[pd.to_datetime(start_date): pd.to_datetime(end_date)]

    # Still empty -> return empty
    if df is None or df.empty:
        return pd.DataFrame(columns=["Close"])

    # normalize to Close only
    if "Close" in df.columns:
        df = df[["Close"]]
    elif "Adj Close" in df.columns:
        df = df[["Adj Close"]].rename(columns={"Adj Close": "Close"})
    else:
        return pd.DataFrame(columns=["Close"])

    df = data_process(df)
    return df



