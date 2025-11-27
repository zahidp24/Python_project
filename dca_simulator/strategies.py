import pandas as pd

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


    ##Performance measures
    #Profit/Loss
    monthly_investments['profit_loss'] = monthly_investments['portf_value'] - monthly_investments['invested_total']
    

    final_value = monthly_investments["portf_value"].iloc[-1]
    final_invested = monthly_investments["invested_total"].iloc[-1]

    #Return on Investment (ROI)
    ROI = (final_value/final_invested - 1)*100

    #Cumilative Annual Growth Rate (CAGR)
    years = (monthly_investments.index[-1] - monthly_investments.index[0]).days/365 
    CAGR = ((final_value/final_invested)**(1/years) - 1)*100
    
    print(f"ROI: {ROI:.2f}%")
    print(f"CAGR: {CAGR:.2f}%")

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


    ##Performance measures
    #Profit/Loss
    monthly_investments['profit_loss'] = monthly_investments['portf_value'] - monthly_investments['invested_total']
    

    final_value = monthly_investments["portf_value"].iloc[-1]
    final_invested = monthly_investments["invested_total"].iloc[-1]

    #Return on Investment (ROI)
    ROI = (final_value/final_invested - 1)*100

    #Cumilative Annual Growth Rate (CAGR)
    years = (monthly_investments.index[-1] - monthly_investments.index[0]).days/365 
    CAGR = ((final_value/final_invested)**(1/years) - 1)*100
    
    print(f"ROI: {ROI:.2f}%")
    print(f"CAGR: {CAGR:.2f}%")
    

    return monthly_investments
