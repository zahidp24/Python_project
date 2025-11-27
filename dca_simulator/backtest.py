import pandas as pd

def perf_backtest(df, strategy, **strategy_kwargs):
    """Function to perform a certain strategy"""

    result = strategy(df, **strategy_kwargs)
    return result






####the code below was an attempt to match the starting dates and dropna from dca_DD
#def common_start(df):
    """Returns the earliest date where strategies can be compared correctly"""
    #for example the dca_DD requires 252 trading days to calculate first 12m_high
    #this leads to uneven start dates among strategies

    rolling_high = df["Close"].rolling(252).max()
    valid_start = rolling_high.dropna().index[0]
    return valid_start



#def perf_backtest(df, strategy, **strategy_kwargs):
    """Function to perform a certain strategy"""

    start_date = common_start(df)
    df_aligned = df.loc[df.index >= start_date].copy()

    result = strategy(df_aligned, **strategy_kwargs)
    return result