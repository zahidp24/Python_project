import pandas as pd

def dca_DD(df: pd.DataFrame, monthly_contrib: float, DD_threshold: float=0.2):
    """Double Down DCA: Investing monthly_contrib, 
    unless the price is 20% below the rolling 1-year high,
    then invest 2x monthly_contrib"""

    df = df.copy()

    df["12m_high"] = df["Close"].rolling(252).max() #252 trading days in a year
    df["drawdown"] = df["Close"]/df["12m_high"]
    df["DD_cond"] = df["drawdown"] <= (1-DD_threshold) #This is True when the stock is >=20% down from 12m_high

    df = df.dropna(subset=["12m_high"]).copy() #because the 1y rolling high will be NaN for the first year

    monthly_investments = df.resample("MS").first() #because if we specify an exact date manually it could be a non-trading day
    #we buy at the first trading day of each month
    monthly_investments["DD_cond"] = (monthly_investments['Close']/monthly_investments['12m_high'] <= (1-DD_threshold))


    shares_total = 0
    invested_total = 0

    for date, row in monthly_investments.iterrows():
        multiplier = 2 if row["DD_cond"] else 1
        investment_amount = monthly_contrib * multiplier
        #doubling the contribution every time the price drops 20% from rolling high

        shares_bought = investment_amount/row["Close"]
        shares_total += shares_bought
        invested_total += investment_amount

        monthly_investments.loc[date, 'shares_total'] = shares_total
        monthly_investments.loc[date, 'invested_total'] = invested_total
        monthly_investments.loc[date, 'portf_value'] = shares_total * row['Close']

    monthly_investments['profit_loss'] = monthly_investments['portf_value'] - monthly_investments['invested_total']
    return monthly_investments

    

