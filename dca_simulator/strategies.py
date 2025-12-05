import pandas as pd


def dca_DD(df, monthly_contrib: float, DD_threshold: float=0.15):
    """Double Down Dollar-Cost Averaging (DD_DCA): Investing monthly_contrib, 
    unless the price is 15% below the rolling 1-year high,
    then invest 2x monthly_contrib"""

    df = df.copy()

    df["12m_high"] = df["Close"].rolling(252).max() #252 trading days in a year
    df["drawdown"] = df["Close"]/df["12m_high"]
    df["DD_cond"] = df["drawdown"] <= (1-DD_threshold) #This is True when the stock is >=20% down from 12m_high

    

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


    return monthly_investments



def dca_sma_mom(df, monthly_contrib: float, sma_period: int = 90):
    """Simple Moving Average DCA
    Invest an amount (monthly_contrib) only when the price is above the X-day Simple Moving Average, investing in momentum"""

    df = df.copy()
    df["sma"] = df["Close"].rolling(sma_period).mean()
    df["above_sma"] = df["Close"] > df["sma"] #we invest during uptrends, when momentum is high

    monthly_investments = df.resample("MS").first()
    monthly_investments["above_sma"] = df["above_sma"].resample("MS").first()

    shares_total = 0
    invested_total = 0

    for date, row in monthly_investments.iterrows():
        if row["above_sma"] == True:
            shares_bought = monthly_contrib/row["Close"]
            shares_total += shares_bought
            invested_total += monthly_contrib

        monthly_investments.loc[date, "shares_total"] = shares_total
        monthly_investments.loc[date, "invested_total"] = invested_total
        monthly_investments.loc[date, "portf_value"] = shares_total*row["Close"]
    
    monthly_investments["profit_loss"] = monthly_investments["portf_value"] - monthly_investments["invested_total"]


    return monthly_investments



def dca_sma_mean_rev(df, monthly_contrib: float, sma_period: int = 90):
    """Simple Moving Average DCA
    Invest an amount (monthly_contrib) only when the price is above the X-day Simple Moving Average"""

    df = df.copy()
    df["sma"] = df["Close"].rolling(sma_period).mean()
    df["above_sma"] = df["Close"] < df["sma"] #negative exposure to momentum (mean reversion)
    monthly_investments = df.resample("MS").first()
    monthly_investments["above_sma"] = df["above_sma"].resample("MS").first() ########do we actually need those two lines

    shares_total = 0
    invested_total = 0

    for date, row in monthly_investments.iterrows():
        if row["above_sma"] == True:
            shares_bought = monthly_contrib/row["Close"]
            shares_total += shares_bought
            invested_total += monthly_contrib

        monthly_investments.loc[date, "shares_total"] = shares_total
        monthly_investments.loc[date, "invested_total"] = invested_total
        monthly_investments.loc[date, "portf_value"] = shares_total*row["Close"]
    
    monthly_investments["profit_loss"] = monthly_investments["portf_value"] - monthly_investments["invested_total"]


    return monthly_investments


def value_averaging(df, goal_monthly_growth: float=0.006, monthly_contrib = 1000):
    """Value Averaging: portfolio attempts to grow at a constant rate (~0.6%/month = 7.44%/year),
    Invest when below the goal, do not invest when above"""

    df = df.copy()
    monthly_investments = df.resample("MS").first()

    shares_total = 0
    invested_total = 0

    for i, (date, row) in enumerate(monthly_investments.iterrows()):
        goal_val = monthly_contrib*(1+i)*(1+goal_monthly_growth)**i
        current_val = shares_total * row["Close"]

        investment_this_month = max(goal_val - current_val, 0) #we invest if we are behind target and do nothing if we are on track/ahead

        if investment_this_month > 0:
            shares_bought = investment_this_month / row["Close"]
            shares_total += shares_bought
            invested_total += investment_this_month
        
        monthly_investments.loc[date, "shares_total"] = shares_total
        monthly_investments.loc[date, "invested_total"] = invested_total
        monthly_investments.loc[date, "portf_value"] = shares_total*row["Close"]

    monthly_investments["profit_loss"] = monthly_investments["portf_value"] - monthly_investments["invested_total"]


    return monthly_investments
        