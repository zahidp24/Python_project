import pandas as pd

def data_process(df: pd.DataFrame):
    df = df.copy().dropna() #to ensure that our strategies do not break if trying to invest on a day with missing data
    
    if not isinstance(df.index, pd.DatetimeIndex): #ensure that the index is DatetimeIndex
        df.index = pd.to_datetime(df.index)
    
    df = df.sort_index()
    
    return df
    


