import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base Paths (with environment variable overrides)
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "outputs"))
LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))

DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_TRANSCRIPTS_DIR = DATA_DIR / "transcripts"

# Create directories explicitly
for path in [DATA_RAW_DIR, DATA_PROCESSED_DIR, DATA_TRANSCRIPTS_DIR, OUTPUT_DIR, LOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Required Environment Variables (Fail-fast check)
def get_required_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        logger.error(f"CRITICAL: Missing required environment variable: {key}")
        raise EnvironmentError(f"Missing mandatory configuration: {key}")
    return val

# Sensitivity Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Optional if only running financial part, but tracked here
SEC_USER_AGENT = get_required_env("SEC_USER_AGENT")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# SEC Ingestion Logic
CIK_MAPPING = {
    "AAPL": 320193, "MSFT": 789019, "NVDA": 1045810,
    "TSLA": 1318605, "META": 1326801, "GOOGL": 1652044,
    "AMZN": 1018724, "NFLX": 1065280,
    "CAT": 18230, "DE": 31518, "F": 37996, "GM": 1467867,
    "PG": 80424, "KO": 21334, "WMT": 104169, "JNJ": 53427,
    "JPM": 19617, "BAC": 70858, "GS": 886982, "MS": 895421,
    "XOM": 34013, "CVX": 93461, "COP": 1163165, "SLB": 87347
}

SEC_HEADERS = {
    "User-Agent": SEC_USER_AGENT
}

# Analytical Weights
MOMENTUM_WEIGHTS = {
    "financial": {
        "revenue_growth": 0.3,
        "ocf_growth": 0.4,
        "accrual_ratio": 0.3
    },
    "narrative": {
        "optimism": 0.6,
        "risk": 0.4
    }
}

# Guardrails
GROWTH_LIMIT = 2.0  # ±200%
MOMENTUM_LIMIT = 3.0

# LLM Parameters
LLM_CONFIG = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "seed": 42,
    "max_tokens": 1000
}

# Rate Limiting (SEC defaults to 10 requests per second)
SEC_REQUEST_RATE_LIMIT = 0.1 # seconds between requests
