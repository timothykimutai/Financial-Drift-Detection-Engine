import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import financials, narrative, drift
from app.models.schemas import HealthResponse, DriftResponse

# Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Financial Narrative Drift API",
    description="Deterministic quantitative analysis engine for corporate narrative divergence.",
    version="1.0.0"
)

# CORS Policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(financials.router, prefix="/v1/financials", tags=["Financials"])
app.include_router(narrative.router, prefix="/v1/narrative", tags=["Narrative"])
app.include_router(drift.router, prefix="/v1/drift", tags=["Drift"])

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    logger.info("Drift Engine API Initialized")
