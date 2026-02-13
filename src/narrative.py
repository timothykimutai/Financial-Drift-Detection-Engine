import os
import json
import logging
import re
from typing import Dict, Any, Optional
try:
    import openai
except ImportError:
    openai = None

from src.config import LLM_CONFIG, DATA_TRANSCRIPTS_DIR

logger = logging.getLogger(__name__)

try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    class BaseModel: pass
    def Field(*args, **kwargs): return None

class NarrativeSignals(BaseModel):
    """Structural schema for narrative signal extraction."""
    optimism: float = Field(..., ge=-1.0, le=1.0)
    risk: int = Field(..., ge=0)

class NarrativeProcessor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        if openai and self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)

    def clean_and_persist(self, ticker: str, fiscal_period: str, raw_text: str) -> str:
        """Standardizes transcript text and persists to data/transcripts/."""
        if not raw_text: return ""
        
        # Strip boilerplate and non-speech metadata (e.g., "John Doe:", "Operator:")
        text = re.sub(r'^\s*[A-Z][a-zA-Z\s.-]+:', '', raw_text, flags=re.MULTILINE)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Save clean version
        safe_period = fiscal_period.replace(" ", "_").lower()
        clean_path = DATA_TRANSCRIPTS_DIR / f"{ticker}_{safe_period}_clean.txt"
        with open(clean_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return text

    def extract_signals(self, text: str) -> Dict[str, Any]:
        """Deterministic signal extraction (temperature=0) using LLM with Pydantic validation."""
        if not self.client:
            return self._baseline()

        try:
            response = self.client.chat.completions.create(
                model=LLM_CONFIG["model"],
                messages=[
                    {"role": "system", "content": "Analytical Quant. JSON only."},
                    {"role": "user", "content": f"Extract: optimism (float -1 to 1), risk (int). TEXT: {text[:10000]}"}
                ],
                temperature=LLM_CONFIG["temperature"],
                seed=LLM_CONFIG["seed"],
                response_format={"type": "json_object"}
            )
            raw_data = json.loads(response.choices[0].message.content)
            
            # Pydantic Structural Validation
            signals = NarrativeSignals(**raw_data)
            return signals.model_dump()
            
        except (ValidationError, ValueError, json.JSONDecodeError) as e:
            logger.warning(f"STRUCTURAL VALIDATION FAILED | Narrative output malformed: {e}")
            return self._baseline()
        except Exception as e:
            logger.error(f"LLM EXTRACTION ERROR | {e}")
            return self._baseline()

    def _baseline(self) -> Dict[str, Any]:
        return {"optimism": 0.0, "risk": 0}
