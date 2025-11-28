import pandas as pf


def compute_roi(final_value: float, final_invested: float):
    """Computing Return on Investment in %"""
    
    return (final_value/final_invested - 1)*100




#include irr?



###def compute_cagr(final_value: float, final_invested: float, start_date, end_date):
    """Computing Cumilative Average Growth Rate in %"""

    years = (end_date - start_date).days/365  
    return ((final_value/final_invested)**(1/years) - 1)*100
    
