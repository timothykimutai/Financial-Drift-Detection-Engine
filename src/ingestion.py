import requests
import json
import logging
import time
import pandas as pd
from typing import Optional, Dict, Any
from src.config import CIK_MAPPING, SEC_HEADERS, DATA_RAW_DIR, SEC_REQUEST_RATE_LIMIT

logger = logging.getLogger(__name__)

def fetch_raw_sec_data(ticker: str) -> Optional[Dict[str, Any]]:
    """Retrieves raw XBRL facts from SEC with caching and rate limiting."""
    cik = CIK_MAPPING.get(ticker)
    if not cik:
        logger.error(f"Incomplete CIK mapping for {ticker}")
        return None

    # check cache first
    raw_path = DATA_RAW_DIR / f"{ticker}_raw.json"
    if raw_path.exists():
        logger.info(f"Loading cached raw data for {ticker} from {raw_path}")
        with open(raw_path, 'r') as f:
            return json.load(f)

    # SEC limits requests to 10 per second
    time.sleep(SEC_REQUEST_RATE_LIMIT)

    cik_padded = str(cik).zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"

    max_retries = 3
    backoff = 1.0 # initial backoff in seconds

    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching raw data from SEC for {ticker} (Attempt {attempt+1})")
            response = requests.get(url, headers=SEC_HEADERS)
            response.raise_for_status()
            data = response.json()
            
            # Persistence discipline: save raw payload
            with open(raw_path, 'w') as f:
                json.dump(data, f)
            logger.info(f"Raw data persisted for {ticker} at {raw_path}")
            
            return data
        except requests.exceptions.RequestException as e:
            if response.status_code == 429: # Too many requests
                logger.warning(f"Rate limited by SEC. Backing off for {backoff}s")
                time.sleep(backoff)
                backoff *= 2 # Exponential backoff
            else:
                logger.error(f"Ingestion failed for {ticker}: {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(backoff)
    return None

def extract_facts_to_df(ticker: str, data: Dict[str, Any]) -> pd.DataFrame:
    """Converts raw JSON facts to a flattened DataFrame for normalization."""
    facts = data.get("facts", {}).get("us-gaap", {})
    records = []
    
    # Extraction logic with unit and scaling awareness
    for metric_name, metric_data in facts.items():
        units_dict = metric_data.get("units", {})
        # Prioritize USD for financial metrics, fall back to pure numbers if applicable
        target_unit = "USD" if "USD" in units_dict else next(iter(units_dict)) if units_dict else None
        
        if not target_unit: continue
        
        for entry in units_dict[target_unit]:
            if entry.get("form") in ["10-K", "10-Q"]:
                records.append({
                    "ticker": ticker,
                    "metric": metric_name,
                    "value": entry.get("val"),
                    "unit": target_unit,
                    "decimals": entry.get("decimals"),
                    "filed": entry.get("filed"),
                    "fy": entry.get("fy"),
                    "fp": entry.get("fp")
                })
    
    df = pd.DataFrame(records)
    if not df.empty:
        # Log scaling diversity if detected
        unique_decimals = df["decimals"].unique()
        if len(unique_decimals) > 5:
            logger.warning(f"HIGH SCALE DIVERSITY | {ticker} | Detected multiple precision levels ({unique_decimals}).")
    
    return df
