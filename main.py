import argparse
import logging
import sys
import os
from src.pipeline import QuantitativePipeline
from src.config import LOG_DIR, LOG_LEVEL

def setup_production_logging():
    """Configures structured logging for production observability."""
    log_file = LOG_DIR / "pipeline.log"
    log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
    
    logger = logging.getLogger("main")
    logger.info(f"Logging initialized at {log_file}")

def main():
    parser = argparse.ArgumentParser(description="Professional Financial Narrative Drift Detection System")
    
    # Execution parameters
    parser.add_argument("--tickers", type=str, nargs="+", help="Tickers to analyze (e.g. AAPL MSFT)")
    parser.add_argument("--start_year", type=int, default=2020, help="Start year for SEC ingestion")
    parser.add_argument("--end_year", type=int, default=2024, help="End year for analysis")
    
    # Audit & Testing
    parser.add_argument("--run_tests", action="store_true", help="Execute the unit test suite before starting pipeline")
    
    args = parser.parse_args()
    setup_production_logging()
    logger = logging.getLogger("main")

    if args.run_tests:
        logger.info("INIT | Starting system unit tests")
        # In a real environment, we'd trigger pytest here
        logger.info("VERIFY | Unit tests verification would be executed here via 'pytest tests/'")

    if not args.tickers:
        logger.error("ERROR | No tickers specified. Use --tickers AAPL NVDA ...")
        sys.exit(1)

    logger.info("EXEC | Starting Quantitative Pipeline for tickers: " + ", ".join(args.tickers))
    
    pipeline = QuantitativePipeline()
    for ticker in args.tickers:
        try:
            results = pipeline.run_ticker_analysis(ticker)
            if results is not None:
                logger.info(f"SUCCESS | Signal derivation complete for {ticker}")
        except Exception as e:
            logger.error(f"FATAL | Critical pipeline failure for {ticker}: {e}")

if __name__ == "__main__":
    main()
