import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base Paths (Relative to backend/app)
APP_DIR = Path(__file__).parent
BASE_DIR = APP_DIR.parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))

DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_TRANSCRIPTS_DIR = DATA_DIR / "transcripts"

# Create directories explicitly
for path in [DATA_RAW_DIR, DATA_PROCESSED_DIR, DATA_TRANSCRIPTS_DIR, LOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Required Environment Variables
def get_env(key: str, default: str = None) -> str:
    return os.getenv(key, default)

OPENAI_API_KEY = get_env("OPENAI_API_KEY")
SEC_USER_AGENT = get_env("SEC_USER_AGENT", "Quantitative Auditor (auditor@example.com)")
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")

# Analytical Constants
growth_limit = 2.0
momentum_limit = 3.0

# SEC Ingestion Configuration
SEC_REQUEST_RATE_LIMIT = 0.1 # seconds between requests
CIK_MAPPING = {
    "AAPL": 320193, "MSFT": 789019, "NVDA": 1045810,
    "TSLA": 1318605, "META": 1326801, "GOOGL": 1652044,
    "AMZN": 1018724, "NFLX": 1065280
}

# Quantitative weights
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

# LLM Parametrization
LLM_CONFIG = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "seed": 42,
    "max_tokens": 1000
}
