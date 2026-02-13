from fastapi import APIRouter, HTTPException
from app.models.schemas import DriftResponse
from app.services.drift_service import DriftService

router = APIRouter()

@router.get("/{ticker}", response_model=DriftResponse)
async def get_drift_analysis(ticker: str):
    """Calculates the current narrative drift score for a security."""
    try:
        return DriftService.get_latest_drift(ticker)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
