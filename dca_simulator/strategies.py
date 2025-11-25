import pandas as pd

def dca_DD(df: pd.DataFrame, monthly_contrib: float, DD_treshold: float=0.2):
    """Double Down DCA when price is 20% below the rolling 1-year high"""

    df = df.copy()
    df["12m_high"] = df["Close"].rolling(252).max() #252 trading days in a year
    df["DD_cond"] = df["Close"] <= (1-DD_treshold) * df["12m_high"]

    monthly_price = df.resample("M").first() #because if we specify an exact date manually it could be a non-trading day
    #we buy at the first trading day of each month

    shares = []
    invested = []
    shares_total = 0
    invested_total = 0

    for date, row in monthly_price.iterrows():
        price = row["Close"]

        investment_amount = monthly_contrib * (2 if row["DD_cond"] else 1)
        #doubling the contribution every time the price drops 20% from rolling high

        shares_bought = investment_amount/price
        shares_total += shares_bought
        invested_total += investment_amount

        shares.append(shares_total)
        invested.append(invested_total)

    result = monthly_price.copy()
    result["shares_total"] = shares #putting the results into the df monthly_price
    result["invested_total"] = invested
    result["portf_value"] = result["shares_total"]*result["Close"]
    result["profit_loss"] = result["porf_value"] - result["invested_total"]
    return result

