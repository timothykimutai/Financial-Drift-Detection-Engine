import re
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def clean_transcript_text(raw_text: str) -> str:
    """Standardizes transcript text by removing boilerplate and speaker labels."""
    if not raw_text:
        return ""
        
    # Remove speaker labels (e.g., "John Doe:", "Operator:")
    text = re.sub(r'^\s*[A-Z][a-zA-Z\s.-]+:', '', raw_text, flags=re.MULTILINE)
    
    # Remove analyst questions/interjections (Q&A section patterns)
    text = re.sub(r'Question-and-Answer Session.*', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def normalize_narrative_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures narrative signals are within bounded limits for drift comparison."""
    if df.empty:
        return df
        
    df = df.copy()
    
    # Bounding optimism
    if "optimism" in df.columns:
        df["optimism"] = df["optimism"].clip(-1.0, 1.0)
        
    # Calculating deltas for momentum
    df["optimism_delta"] = df["optimism"].diff().fillna(0)
    df["risk_delta"] = df["risk"].diff().fillna(0) if "risk" in df.columns else 0
    
    return df
