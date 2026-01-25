import pandas as pd
import numpy as np
import numpy_financial as npf

def compute_KeyMetrics(df):
    """Computes all Key Metrics at once""" ######improve descrip

    final_value = df["portf_value"].iloc[-1]
    final_invested = df["invested_total"].iloc[-1]
    ROI = (final_value/final_invested - 1)*100


    start_date = df.index[0]
    end_date = df.index[-1]
    years = (end_date - start_date).days/365 
    CAGR = ((final_value/final_invested)**(1/years) - 1)*100
    

    peak = df["portf_value"].cummax() #calc local peak
    drawdown = df["portf_value"]/peak - 1 #calc drawdown in current period
    max_drawdown = drawdown.min() * 100


    calmar = CAGR/abs(max_drawdown)


    cashflows = []
    cashflows.append(-df["invested_total"].iloc[0])
    cashflows.extend(-df["invested_total"].diff().iloc[1:]) #calc cashflows on each date
    cashflows[-1] += df["portf_value"].iloc[-1] #we liquidate the investment to calc irr
    cashflows = np.array(cashflows)
    irr_monthly = npf.irr(cashflows) 
    irr_annual = ((1+irr_monthly)**12 - 1)*100


    return {
        "Total Invested": f"${final_invested:,.2f}",
        "Final Value": f"${final_value:,.2f}",
        "ROI": f"{ROI:,.2f}%",
        "IRR": f"{irr_annual:,.2f}%",
        "CAGR": f"{CAGR:,.2f}%",
        "Max Drawdown": f"{max_drawdown:,.2f}%",
        "Calmar Ratio": round(calmar, 2),
        "Years": round(years, 1)
    }
