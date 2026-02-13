import pandas as pd
from typing import Dict, Any, List
from app.core.normalization import normalize_financial_data
from app.core.feature_engineering import engineering_financial_features
from app.core.drift_engine import calculate_drift, generate_deterministic_explanation, compute_momentum_vector
from app.core.transcript_parser import normalize_narrative_signals
from app.services.ingestion_service import IngestionService
from app.models.schemas import DriftResponse
from app.config import MOMENTUM_WEIGHTS

class DriftService:
    @staticmethod
    def get_latest_drift(ticker: str) -> DriftResponse:
        """Computes current drift state for a ticker by orchestrating data feeds."""
        # 1. Fetch raw data (orchestrated via IngestionService)
        raw_data = IngestionService.fetch_raw_sec_data(ticker)
        if not raw_data:
            raise ValueError(f"Data unavailable for {ticker}")
            
        # 2. Financial Momentum
        raw_df = IngestionService.extract_facts_to_df(ticker, raw_data)
        
        # 2.1 Normalization (Pivot long-form facts to canonical pillars)
        normalized_df = normalize_financial_data(raw_df)
        if normalized_df.empty:
            raise ValueError(f"Normalization failed for {ticker}")

        # 2.2 Feature Engineering
        processed_df = engineering_financial_features(normalized_df)
        fin_momentum = compute_momentum_vector(processed_df.iloc[-1:], MOMENTUM_WEIGHTS["financial"]).iloc[0]
        
        # 3. Narrative Momentum (Mocking signal extraction for this skeleton)
        # In a real app, this would call NarrativeService.process_transcript()
        nar_signals = pd.DataFrame([{"optimism": 0.3, "risk": 5}, {"optimism": 0.4, "risk": 4}])
        nar_df = normalize_narrative_signals(nar_signals)
        nar_momentum = compute_momentum_vector(nar_df.iloc[-1:], MOMENTUM_WEIGHTS["narrative"]).iloc[0]
        
        # 4. Drift Calculation
        drift_score = calculate_drift(fin_momentum, nar_momentum)
        
        # 5. Result Construction
        row = {
            "drift_score": drift_score,
            "financial_momentum": fin_momentum,
            "narrative_momentum": nar_momentum
        }
        explanation = generate_deterministic_explanation(row)
        
        return DriftResponse(
            ticker=ticker,
            quarter="2023-Q3", # Derived from ingestion data in full impl
            financial_momentum=float(fin_momentum),
            narrative_momentum=float(nar_momentum),
            drift_score=float(drift_score),
            explanation=explanation
        )
