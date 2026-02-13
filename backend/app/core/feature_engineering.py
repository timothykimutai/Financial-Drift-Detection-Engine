import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def engineering_financial_features(df: pd.DataFrame, growth_limit: float = 2.0) -> pd.DataFrame:
    """Calculates accounting quality and growth metrics for a normalized dataset."""
    if df.empty:
        return df

    df = df.copy()

    # 1. Quality Ratios (Accounting Quality Proxies)
    # FCF = OCF - Capex
    df["free_cash_flow"] = df["operating_cash_flow"] - df["capex"]
    
    # Accrual Ratio = (NI - OCF) / Total Assets
    # High positive = Aggressive accounting; Negative = Conservative/high-quality
    df["accrual_ratio"] = (df["net_income"] - df["operating_cash_flow"]) / df["total_assets"]
    
    # OCF Conversion = OCF / NI
    df["ocf_conversion"] = df["operating_cash_flow"] / df["net_income"].replace(0, np.nan)

    # 2. Growth metrics (bounded for stability)
    def pct_change_robust(series):
        return series.pct_change().replace([np.inf, -np.inf], np.nan).clip(-growth_limit, growth_limit)

    df["revenue_growth"] = pct_change_robust(df["revenue"])
    df["ocf_growth"] = pct_change_robust(df["operating_cash_flow"])
    df["ni_growth"] = pct_change_robust(df["net_income"])
    
    # Fill remaining NaNs for calculation stability
    df = df.fillna(0)
    
    return df
