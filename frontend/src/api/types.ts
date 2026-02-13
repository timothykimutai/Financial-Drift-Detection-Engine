export interface FinancialsResponse {
    ticker: str;
    quarterly_index: string[];
    revenue_growth: number[];
    ocf_growth: number[];
    accrual_ratio: number[];
    free_cash_flow: number[];
}

export interface NarrativeResponse {
    ticker: string;
    optimism_score: number[];
    risk_mentions: number[];
    forward_looking_density: number[];
    narrative_momentum: number[];
}

export interface DriftResponse {
    ticker: string;
    quarter: string;
    financial_momentum: number;
    narrative_momentum: number;
    drift_score: number;
    explanation: string;
}
