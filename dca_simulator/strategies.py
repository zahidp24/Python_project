import pandas as pd
from .metrics import compute_roi
####, compute_cagr


def dca_DD(df, monthly_contrib: float, DD_threshold: float=0.15):
    """Double Down Dollar-Cost Averaging (DD_DCA): Investing monthly_contrib, 
    unless the price is 15% below the rolling 1-year high,
    then invest 2x monthly_contrib"""

    df = df.copy()

    df["12m_high"] = df["Close"].rolling(252).max() #252 trading days in a year
    df["drawdown"] = df["Close"]/df["12m_high"]
    df["DD_cond"] = df["drawdown"] <= (1-DD_threshold) #This is True when the stock is >=20% down from 12m_high

    ####df = df.dropna(subset=["12m_high"]).copy() #because the 1y rolling high will be NaN for the first year

    monthly_investments = df.resample("MS").first() #because if we specify an exact date manually it could be a non-trading day
    #we buy at the first trading day of each month
    monthly_investments["DD_cond"] = df["DD_cond"].resample("MS").first()


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


    #Profit/Loss
    monthly_investments['profit_loss'] = monthly_investments['portf_value'] - monthly_investments['invested_total']
    
    final_value = monthly_investments["portf_value"].iloc[-1] #used for metrics calc
    final_invested = monthly_investments["invested_total"].iloc[-1]

    ####start_date = monthly_investments.index[0]
    ####end_date = monthly_investments.index[-1]

    ROI = compute_roi(final_value, final_invested)
    ####CAGR = compute_cagr(final_value, final_invested, start_date, end_date)

    print(f"ROI: {ROI:.2f}%")
    ####print(f"CAGR: {CAGR:.2f}%")
    return monthly_investments

    

def dca_standard(df, monthly_contrib: float):
    """Standard Dollar-Cost Averaging (DCA)"""

    df = df.copy()

    monthly_investments = df.resample("MS").first() #because if we specify an exact date manually it could be a non-trading day
    #we buy at the first trading day of each month


    shares_total = 0
    invested_total = 0

    for date, row in monthly_investments.iterrows():
        investment_amount = monthly_contrib
    

        shares_bought = investment_amount/row["Close"]
        shares_total += shares_bought
        invested_total += investment_amount

        monthly_investments.loc[date, 'shares_total'] = shares_total
        monthly_investments.loc[date, 'invested_total'] = invested_total
        monthly_investments.loc[date, 'portf_value'] = shares_total * row['Close']


    #Profit/Loss
    monthly_investments['profit_loss'] = monthly_investments['portf_value'] - monthly_investments['invested_total']
    
    final_value = monthly_investments["portf_value"].iloc[-1]
    final_invested = monthly_investments["invested_total"].iloc[-1]

    ####start_date = monthly_investments.index[0]
    #####end_date = monthly_investments.index[-1]

    ROI = compute_roi(final_value, final_invested)
    ####CAGR = compute_cagr(final_value, final_invested, start_date, end_date)
    print(f"ROI: {ROI:.2f}%")
    ####print(f"CAGR: {CAGR:.2f}%")
    return monthly_investments



def lump_sum(df, monthly_contrib: float):
    "Lump Sum investment strategy: invest all money at the beginning date"
    "monthly_contrib is used as to calculate the total amount that should be invested as a lump sum to be comparable to the Normal DCA"

    df = df.copy()
    monthly_investments = df.resample("MS").first()

    total_months = len(monthly_investments)
    total_capital = total_months*monthly_contrib #so that the strategy uses the same amount of capital as Normal DCA
    
    first_price = monthly_investments.loc[monthly_investments.index[0], "Close"]
    
    shares_total = total_capital/first_price

    
    monthly_investments["shares_total"] = shares_total
    monthly_investments["invested_total"] = total_capital
    monthly_investments["portf_value"] = shares_total*monthly_investments["Close"]
    monthly_investments["profit_loss"] = (monthly_investments["portf_value"] - total_capital)

    final_value = monthly_investments["portf_value"].iloc[-1]
    final_invested = monthly_investments["invested_total"].iloc[-1]

    ROI = compute_roi(final_value, final_invested)
    print(f"ROI: {ROI:.2f}%")
    return monthly_investments