import os
import json
import logging
from typing import Dict, Any, Optional
import openai
from app.config import LLM_CONFIG, OPENAI_API_KEY, DATA_TRANSCRIPTS_DIR
from app.core.transcript_parser import clean_transcript_text

logger = logging.getLogger(__name__)

class NarrativeService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.client = None
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)

    def process_transcript(self, ticker: str, fiscal_period: str, raw_text: str) -> Dict[str, Any]:
        """Cleans transcript and extracts structured signals."""
        clean_text = clean_transcript_text(raw_text)
        
        # Persist clean text
        safe_period = fiscal_period.replace(" ", "_").lower()
        clean_path = DATA_TRANSCRIPTS_DIR / f"{ticker}_{safe_period}_clean.txt"
        with open(clean_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)
            
        return self.extract_signals(clean_text)

    def extract_signals(self, text: str) -> Dict[str, Any]:
        """Deterministic signal extraction using LLM."""
        if not self.client:
            return {"optimism": 0.0, "risk": 0}

        try:
            response = self.client.chat.completions.create(
                model=LLM_CONFIG["model"],
                messages=[
                    {"role": "system", "content": "Analytical Quant. JSON only. Extract: optimism (float -1 to 1), risk (int)."},
                    {"role": "user", "content": f"TEXT: {text[:10000]}"}
                ],
                temperature=LLM_CONFIG["temperature"],
                seed=LLM_CONFIG["seed"],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"LLM EXTRACTION ERROR | {e}")
            return {"optimism": 0.0, "risk": 0}
