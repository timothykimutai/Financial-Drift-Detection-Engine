import pandas as pd

def generate_drift_explanations(df: pd.DataFrame) -> pd.DataFrame:
    """Produces deterministic textual summaries of the narrative-financial drift."""
    if df.empty: return df
    
    df = df.copy()
    explanations = []
    
    for _, row in df.iterrows():
        drift = row["drift_score"]
        period = f"Q{int(row['fiscal_quarter'])} {int(row['fiscal_year'])}"
        
        if abs(drift) < 0.15:
            type_str = "Neutral/Aligned"
            desc = "Management narrative is structurally aligned with financial momentum."
        elif drift > 0:
            type_str = "Positive Divergence"
            desc = "Management narrative is structurally more optimistic than financial performance metrics suggest."
        else:
            type_str = "Negative Divergence"
            desc = "Management narrative is structurally more conservative than financial performance metrics suggests."
            
        explanations.append(f"[{type_str}] {period}: {desc}")
    
    df["explanation"] = explanations
    return df
