import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Canonical SEC Tag Mapping
PILLAR_MAPPING = {
    "Revenues": "revenue",
    "SalesRevenueNet": "revenue",
    "RevenueFromContractWithCustomerExcludingCostReportedOnSameLineAsRevenue": "revenue",
    "NetIncomeLoss": "net_income",
    "NetIncomeLossAvailableToCommonStockholdersBasic": "net_income",
    "NetCashProvidedByUsedInOperatingActivities": "operating_cash_flow",
    "PaymentsToAcquirePropertyPlantAndEquipment": "capex",
    "Assets": "total_assets"
}

def normalize_financial_data(long_df: pd.DataFrame) -> pd.DataFrame:
    """Pivots SEC facts and maps them to canonical pillars."""
    if long_df.empty:
        return long_df

    # 1. Map tags
    df = long_df.copy()
    df["pillar"] = df["metric"].map(PILLAR_MAPPING)
    
    # Filter for mapped pillars only
    df = df.dropna(subset=["pillar"])
    
    if df.empty:
        logger.warning("No canonical pillars found in raw data")
        return pd.DataFrame()

    # 2. Handle Scaling (using decimals field)
    # Value = val * 10^decimals (usually decimals are negative for millions/thousands)
    # But SEC data is usually already in ones if units=USD.
    # However, for consistency we ensure float type.
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # 3. Pivot to wide format
    # Indexing by ticker, fy, fp, and filed date to ensure uniqueness per period
    pivot_df = df.pivot_table(
        index=["ticker", "fy", "fp", "filed"],
        columns="pillar",
        values="value",
        aggfunc="last"
    ).reset_index()

    # 4. Mandatory Pillar Validation (Fail-fast strategy)
    mandatory_pillars = ["revenue", "net_income", "operating_cash_flow"]
    missing = [p for p in mandatory_pillars if p not in pivot_df.columns]
    
    if missing:
        logger.error(f"DATA INTEGRITY FAILURE | Missing mandatory pillars: {missing}")
        return pd.DataFrame()

    # Fill optional pillars (like capex/assets) with 0 if missing
    for p in ["capex", "total_assets"]:
        if p not in pivot_df.columns:
            pivot_df[p] = 0

    # Sort by filing date
    pivot_df = pivot_df.sort_values("filed")
    
    return pivot_df
