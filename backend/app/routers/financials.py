from fastapi import APIRouter, HTTPException
from app.models.schemas import FinancialsResponse
from app.services.financial_service import FinancialService
import pandas as pd # Mocking data feed for skeleton
from app.services.ingestion_service import IngestionService

router = APIRouter()

@router.get("/{ticker}", response_model=FinancialsResponse)
async def get_financial_metrics(ticker: str):
    """Retrieves quarterly financial quality and growth metrics."""
    try:
        # In a real app, this would fetch from a database or IngestionService
        raw_data = IngestionService.fetch_raw_sec_data(ticker)
        if not raw_data:
            raise HTTPException(status_code=404, detail=f"Data for {ticker} not found.")
            
        raw_df = IngestionService.extract_facts_to_df(ticker, raw_data)
        return FinancialService.get_financial_metrics(ticker, raw_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
