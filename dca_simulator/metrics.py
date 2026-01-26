import pandas as pd
import numpy as np
import numpy_financial as npf

def compute_KeyMetrics(df: pd.DataFrame) -> dict:
    """Compute summary performance metrics from a strategy output dataframe.
    Expected columns: portf_value, invested_total. Index must be datetime-like.
    """

    if df is None or df.empty:
        return {
            "Total Invested": "—",
            "Final Value": "—",
            "ROI": "—",
            "IRR": "—",
            "CAGR": "—",
            "Max Drawdown": "—",
            "Calmar Ratio": "—",
            "Years": "—",
        }

    final_value = float(df["portf_value"].iloc[-1])
    final_invested = float(df["invested_total"].iloc[-1])

    start_date = df.index[0]
    end_date = df.index[-1]
    years = (end_date - start_date).days / 365

    # ROI / CAGR guards
    if final_invested <= 0 or years <= 0:
        ROI = np.nan
        CAGR = np.nan
    else:
        ROI = (final_value / final_invested - 1) * 100
        CAGR = ((final_value / final_invested) ** (1 / years) - 1) * 100

    # Drawdown
    peak = df["portf_value"].cummax()
    drawdown = df["portf_value"] / peak - 1
    max_drawdown = float(drawdown.min() * 100)

    # Calmar
    if max_drawdown == 0 or pd.isna(CAGR):
        calmar = np.nan
    else:
        calmar = float(CAGR / abs(max_drawdown))

    # IRR (monthly cashflows)
    irr_annual = np.nan
    try:
        cashflows = []
        cashflows.append(-float(df["invested_total"].iloc[0]))
        cashflows.extend((-df["invested_total"].diff().iloc[1:]).astype(float).tolist())
        cashflows[-1] += final_value
        cashflows = np.array(cashflows, dtype=float)

        irr_monthly = npf.irr(cashflows)
        if irr_monthly == irr_monthly:  # not nan
            irr_annual = ((1 + irr_monthly) ** 12 - 1) * 100
    except Exception:
        pass

    return {
        "Total Invested": f"${final_invested:,.2f}",
        "Final Value": f"${final_value:,.2f}",
        "ROI": f"{ROI:,.2f}%" if ROI == ROI else "—",
        "IRR": f"{irr_annual:,.2f}%" if irr_annual == irr_annual else "—",
        "CAGR": f"{CAGR:,.2f}%" if CAGR == CAGR else "—",
        "Max Drawdown": f"{max_drawdown:,.2f}%",
        "Calmar Ratio": round(calmar, 2) if calmar == calmar else "—",
        "Years": round(years, 1) if years == years else "—",
    }




#def compute_roi(df):
    """Computing Return on Investment (%)"""

    final_value = df["portf_value"].iloc[-1]
    final_invested = df["invested_total"].iloc[-1]
    ROI = (final_value/final_invested - 1)*100
    return ROI





#def compute_cagr(df):
    """Computing Compound Annual Growth Rate (%) - average growth rate per year"""
    #the definition below differs slighly from classical CAGR since we are continuosly investing
    #whereas classic CAGR is calculated as (end_value/start_value - 1)**(1/years)

    start_date = df.index[0]
    end_date = df.index[-1]
    years = (end_date - start_date).days/365 
    final_value = df["portf_value"].iloc[-1]
    final_invested = df["invested_total"].iloc[-1] 
    CAGR = ((final_value/final_invested)**(1/years) - 1)*100
    return CAGR
    


#def compute_max_drawdown(df):
    """Maximum Drawdown (%) - the largest percentage loss from a peak to a trough in the value of the investment"""

    peak = df["portf_value"].cummax() #calc local peak
    drawdown = df["portf_value"]/peak - 1 #calc drawdown in current period
    max_drawdown = drawdown.min() * 100
    return max_drawdown
   



#def compute_calmar(df):
    
    start_date = df.index[0]
    end_date = df.index[-1]
    years = (end_date - start_date).days/365

    final_value = df["portf_value"].iloc[-1]
    final_invested = df["invested_total"].iloc[-1] 
    CAGR = ((final_value/final_invested)**(1/years) - 1)*100


    peak = df["portf_value"].cummax() 
    drawdown = df["portf_value"]/peak - 1 
    max_drawdown = drawdown.min() * 100

    calmar = CAGR/abs(max_drawdown)
    return calmar



#def compute_irr(df):
    """Compute Internal Rate of Return (IRR), the discount rate that makes the PV of all cashflows equal 0"""

    cashflows = []

    cashflows.append(-df["invested_total"].iloc[0])
    cashflows.extend(-df["invested_total"].diff().iloc[1:]) #calc cashflows on each date

    cashflows[-1] += df["portf_value"].iloc[-1] #we liquidate the investment to calc irr

    cashflows = np.array(cashflows)

    irr_daily = npf.irr(cashflows) 
    irr_annual = ((1+irr_daily)**365 - 1)*100
    return irr_annual



#####fix days to 252
