import pandas as pd
import logging
import time
from datetime import datetime
from typing import List, Optional
from src.config import OUTPUT_DIR
from src.ingestion import fetch_raw_sec_data, extract_facts_to_df
from src.normalization import normalize_sec_metrics
from src.features import engineering_financial_features
from src.narrative import NarrativeProcessor
from src.drift import calculate_momentum_scores, derive_drift_signal
from src.reporting import generate_drift_explanations
from src.visualization import generate_visual_artifacts

logger = logging.getLogger(__name__)

class QuantitativePipeline:
    """Orchestrates the data flow of the research-grade drift detection system."""
    
    def __init__(self):
        self.narrative_proc = NarrativeProcessor()

    def run_ticker_analysis(self, ticker: str) -> Optional[pd.DataFrame]:
        """Coordinates the end-to-end analytical lifecycle for a single security."""
        start_time = time.time()
        logger.info(f"START | {ticker} | Initiating full analytical pipeline")
        
        try:
            # 1. Ingestion
            logger.info(f"STAGE | {ticker} | Ingestion")
            raw_facts = fetch_raw_sec_data(ticker)
            if not raw_facts: 
                logger.error(f"FAILURE | {ticker} | Raw facts ingestion returned None")
                return None
            facts_df = extract_facts_to_df(ticker, raw_facts)
            
            # 2. Normalization
            logger.info(f"STAGE | {ticker} | Normalization")
            norm_df = normalize_sec_metrics(facts_df)
            if norm_df.empty: 
                logger.error(f"FAILURE | {ticker} | Normalization returned empty DataFrame")
                return None
            
            # 3. Feature Engineering
            logger.info(f"STAGE | {ticker} | Feature Engineering")
            features_df = engineering_financial_features(norm_df)
            
            # 4. Narrative Extraction
            logger.info(f"STAGE | {ticker} | Narrative Extraction")
            narrative_data = []
            for _, row in features_df.iterrows():
                # simulate signals
                signals = self.narrative_proc._baseline()
                signals.update({
                    "ticker": ticker,
                    "fiscal_year": row["fiscal_year"],
                    "fiscal_quarter": row["fiscal_quarter"]
                })
                narrative_data.append(signals)
            
            narrative_df = pd.DataFrame(narrative_data)
            
            # 5. Drift Computation
            logger.info(f"STAGE | {ticker} | Drift Computation")
            merged_df = pd.merge(features_df, narrative_df, on=["ticker", "fiscal_year", "fiscal_quarter"])
            momentum_df = calculate_momentum_scores(merged_df)
            drift_df = derive_drift_signal(momentum_df)
            
            # 6. Reporting & Explanations
            logger.info(f"STAGE | {ticker} | Reporting")
            final_df = generate_drift_explanations(drift_df)
            
            # 7. Visualization & Persistence
            logger.info(f"STAGE | {ticker} | Persistence & Visualization")
            self._finalize_outputs(ticker, final_df)
            
            duration = time.time() - start_time
            logger.info(f"SUCCESS | {ticker} | Pipeline completed in {duration:.2f}s")
            return final_df

        except (ValueError, KeyError) as e:
            logger.warning(f"DATA INTEGRITY FAILED | {ticker} | {str(e)}")
            return None
        except Exception as e:
            logger.error(f"RUNTIME ERROR | {ticker} | {str(e)}", exc_info=True)
            return None

    def _finalize_outputs(self, ticker: str, df: pd.DataFrame):
        """Saves final analytical artifacts and triggers chart generation with versioning."""
        version_date = datetime.now().strftime("%Y%m%d")
        ticker_output = OUTPUT_DIR / ticker / version_date
        ticker_output.mkdir(parents=True, exist_ok=True)
        
        # Save analysis CSV
        analysis_path = ticker_output / "drift_analysis.csv"
        df.to_csv(analysis_path, index=False)
        
        # Trigger visualization (passing versioned dir)
        generate_visual_artifacts(df, ticker, ticker_output)
        
        logger.info(f"PERSISTENCE | {ticker} | Artifacts versioned at {ticker_output}")
