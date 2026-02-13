import pandas as pd
import numpy as np
import logging
from src.config import MOMENTUM_WEIGHTS, MOMENTUM_LIMIT

logger = logging.getLogger(__name__)

def calculate_momentum_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Computes capped momentum components based on financial and narrative deltas."""
    if df.empty: return df
    
    df = df.copy()
    w_fin = MOMENTUM_WEIGHTS["financial"]
    w_nar = MOMENTUM_WEIGHTS["narrative"]

    # 1. Financial Momentum (acceleration in quality/growth metrics)
    df["financial_momentum"] = (
        w_fin["revenue_growth"] * df["revenue_growth"].fillna(0) +
        w_fin["ocf_growth"] * df["ocf_growth"].fillna(0) +
        w_fin["accrual_ratio"] * df["accrual_ratio_delta"].fillna(0)
    ).clip(-MOMENTUM_LIMIT, MOMENTUM_LIMIT)

    # 2. Narrative Momentum (sentiment trajectory)
    # Ensure deltas exist before weighting
    if "optimism_delta" not in df.columns:
        df["optimism_delta"] = df.groupby("ticker")["optimism"].diff().fillna(0)
    if "risk_delta" not in df.columns:
        df["risk_delta"] = df.groupby("ticker")["risk"].diff().fillna(0)

    df["narrative_momentum"] = (
        w_nar["optimism"] * df["optimism_delta"] - 
        w_nar["risk"] * df["risk_delta"]
    ).clip(-MOMENTUM_LIMIT, MOMENTUM_LIMIT)

    return df

def derive_drift_signal(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates final drift score: narrative lead/lag relative to financials."""
    if df.empty: return df
    
    df["drift_score"] = df["narrative_momentum"] - df["financial_momentum"]
    return df
