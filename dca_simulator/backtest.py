import pandas as pd

def perf_backtest(df: pd.DataFrame, strategy, **strategy_kwargs):
    """Function to perform a certain strategy"""

    result = strategy(df, **strategy_kwargs)
    return result





