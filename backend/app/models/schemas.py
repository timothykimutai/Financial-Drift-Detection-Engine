from pydantic import BaseModel
from typing import List, Optional

class FinancialsResponse(BaseModel):
    ticker: str
    quarterly_index: List[str]
    revenue_growth: List[float]
    ocf_growth: List[float]
    accrual_ratio: List[float]
    free_cash_flow: List[float]

class NarrativeResponse(BaseModel):
    ticker: str
    optimism_score: List[float]
    risk_mentions: List[int]
    forward_looking_density: List[float]
    narrative_momentum: List[float]

class DriftResponse(BaseModel):
    ticker: str
    quarter: str
    financial_momentum: float
    narrative_momentum: float
    drift_score: float
    explanation: str

class HealthResponse(BaseModel):
    status: str
    version: str
