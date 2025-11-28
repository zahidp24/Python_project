import pandas as pd

def data_process(df: pd.DataFrame):
    df = df.copy().dropna() #to ensure that our strategies do not break if trying to invest on a day with missing data
    return df
    


