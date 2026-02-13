import pandas as pd
from typing import List
from app.core.normalization import normalize_financial_data
from app.core.feature_engineering import engineering_financial_features
from app.models.schemas import FinancialsResponse

class FinancialService:
    @staticmethod
    def get_financial_metrics(ticker: str, raw_df: pd.DataFrame) -> FinancialsResponse:
        """Processes raw financial data into structured metrics."""
        # 1. Pivot and Map to Canonical Pillars
        normalized_df = normalize_financial_data(raw_df)
        if normalized_df.empty:
            raise ValueError(f"Failed to normalize financial data for {ticker}")

        # 2. Compute Engineering Features
        df = engineering_financial_features(normalized_df)
        
        return FinancialsResponse(
            ticker=ticker,
            quarterly_index=df.index.astype(str).tolist(),
            revenue_growth=df["revenue_growth"].fillna(0).tolist(),
            ocf_growth=df["ocf_growth"].fillna(0).tolist(),
            accrual_ratio=df["accrual_ratio"].fillna(0).tolist(),
            free_cash_flow=df["free_cash_flow"].fillna(0).tolist()
        )
