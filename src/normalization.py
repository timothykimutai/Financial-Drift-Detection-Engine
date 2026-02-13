import pandas as pd
import numpy as np
import logging
from src.config import DATA_PROCESSED_DIR

logger = logging.getLogger(__name__)

CANONICAL_SCHEMA = [
    "revenue", "net_income", "operating_cash_flow", 
    "total_assets", "accounts_receivable", 
    "share_based_compensation", "capex"
]

METRIC_MAP = {
    "Revenues": "revenue",
    "RevenueFromContractWithCustomerExcludingAssessedTax": "revenue_alt",
    "NetIncomeLoss": "net_income",
    "NetCashProvidedByUsedInOperatingActivities": "operating_cash_flow",
    "Assets": "total_assets",
    "AccountsReceivableNetCurrent": "accounts_receivable",
    "ShareBasedCompensation": "share_based_compensation",
    "PaymentsToAcquirePropertyPlantAndEquipment": "capex"
}

def normalize_sec_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms raw facts to canonical wide format and persists to data/processed/."""
    if df.empty:
        return pd.DataFrame()

    ticker = df["ticker"].iloc[0]
    
    # Filing priority logic
    df = df.sort_values(by=["fy", "fp", "metric", "filed"], ascending=False)
    df = df.drop_duplicates(subset=["fy", "fp", "metric"], keep="first")

    # Wide conversion
    norm_df = df.pivot(index=["ticker", "fy", "fp"], columns="metric", values="value")
    norm_df = norm_df.rename(columns=METRIC_MAP)

    # Consolidation
    if "revenue" not in norm_df.columns: norm_df["revenue"] = np.nan
    if "revenue_alt" in norm_df.columns:
        norm_df["revenue"] = norm_df["revenue"].fillna(norm_df["revenue_alt"])

    # Ensure schema
    for col in CANONICAL_SCHEMA:
        if col not in norm_df.columns:
            norm_df[col] = np.nan

    norm_df = norm_df[CANONICAL_SCHEMA].reset_index()
    norm_df = norm_df.rename(columns={"fy": "fiscal_year", "fp": "fiscal_quarter"})

    # Mandatory Metric Validation (Audit Remediation)
    mandatory_metrics = ["revenue", "operating_cash_flow", "net_income"]
    missing_mandatory = [m for m in mandatory_metrics if norm_df[m].isna().all()]
    if missing_mandatory:
        logger.error(f"SILENT DATA GAP | {ticker} | Missing mandatory metrics: {missing_mandatory}")
        raise ValueError(f"Incomplete financial metadata for {ticker}: {missing_mandatory}")

    # Type enforcement with robust error coercion
    norm_df["fiscal_year"] = pd.to_numeric(norm_df["fiscal_year"], errors='coerce').fillna(0).astype(int)
    norm_df["fiscal_quarter"] = norm_df["fiscal_quarter"].astype(str).str.replace("Q", "").str.extract('(\d+)').fillna(0).astype(int)
    
    # Drop records with invalid fiscal identifiers
    norm_df = norm_df[(norm_df["fiscal_year"] > 2000) & (norm_df["fiscal_quarter"] > 0)]

    # Persistence
    processed_path = DATA_PROCESSED_DIR / f"{ticker}_normalized.csv"
    norm_df.to_csv(processed_path, index=False)
    logger.info(f"Normalized data persisted for {ticker} at {processed_path}")

    return norm_df
