import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def compute_momentum_vector(df: pd.DataFrame, weights: Dict[str, float]) -> pd.Series:
    """Calculates a weighted momentum vector from provided metrics."""
    momentum = pd.Series(0.0, index=df.index)
    for col, weight in weights.items():
        if col in df.columns:
            momentum += df[col] * weight
    return momentum

def calculate_drift(financial_momentum: pd.Series, narrative_momentum: pd.Series) -> pd.Series:
    """Derives the drift score as the divergence between narrative and fiscal momentum."""
    return narrative_momentum - financial_momentum

def generate_deterministic_explanation(row: Dict[str, Any]) -> str:
    """Generates a structured explanation based on quantitative thresholds."""
    drift = row.get("drift_score", 0)
    
    if drift > 0.5:
        return "CRITICAL DIVERGENCE: Narrative optimism significantly outpaces fundamental momentum. Risk of sentiment over-extension."
    elif drift > 0.2:
        return "MODERATE DIVERGENCE: Narrative leading fundamentals. Monitor accrual quality for potential decoupling."
    elif drift < -0.2:
        return "CONSERVATIVE BIAS: Fundamentals outpacing narrative. Potential management sandbagging or excessive risk-aversion."
    else:
        return "STABLE ALIGNMENT: Narrative and fiscal momentum are within nominal variance."
