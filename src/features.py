import pandas as pd
import numpy as np
import logging
from src.config import GROWTH_LIMIT

logger = logging.getLogger(__name__)

def engineering_financial_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates accounting quality and growth metrics for a normalized dataset."""
    if df.empty:
        return df

    df = df.copy()

    # 1. Quality Ratios (Accounting Quality Proxies)
    df["free_cash_flow"] = df["operating_cash_flow"] - df["capex"]
    
    # Growth metrics with robust clipping to handle volatility/zeros
    # Vectorized pct_change with immediate clipping
    def pct_change_robust(series):
        return series.pct_change().replace([np.inf, -np.inf], np.nan).clip(-GROWTH_LIMIT, GROWTH_LIMIT)

    df["revenue_growth"] = df.groupby("ticker")["revenue"].transform(pct_change_robust)
    df["ocf_growth"] = df.groupby("ticker")["operating_cash_flow"].transform(pct_change_robust)
    
    # Accrual persistence
    df["accrual_ratio"] = (df["net_income"] - df["operating_cash_flow"]) / df["total_assets"]
    df["accrual_ratio_delta"] = df.groupby("ticker")["accrual_ratio"].diff()

    # Rolling momentum over 4 quarters
    df["rolling_revenue_growth"] = df.groupby("ticker")["revenue_growth"].transform(lambda x: x.rolling(4, min_periods=4).mean())
    
    return df
