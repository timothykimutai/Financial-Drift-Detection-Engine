# Analytical Platform: Testing & DevOps Strategy

## 1. Multi-Layer Testing Strategy

### A. Core Unit Tests (`backend/app/tests/core/`)
- **Focus**: Mathematical correctness and determinism.
- **Scope**: `feature_engineering.py`, `drift_engine.py`.
- **Requirements**: Verify zero drift score change when inputs are identical. Verify growth clipping at ±200%.

### B. Service/Mock Tests (`backend/app/tests/services/`)
- **Focus**: Orchestration and error handling.
- **Scope**: `ingestion_service.py`, `narrative_service.py`.
- **Mocks**: SEC Edgar API (using `responses` or `pytest-mock`) to simulate offline analysis.

### C. API Integration Tests (`backend/app/tests/test_api.py`)
- **Focus**: Contract enforcement and idempotency.
- **Scope**: FastAPI routers and Pydantic schemas.
- **Baseline**: 100% test pass on `/v1/drift` for standard tickers.

---

## 2. CI/CD Requirements

### Step 1: Analytical Parity Check
Every commit must run a parity suite to ensure the "Drift Score" for a set of benchmark tickers (e.g., NVDA, AAPL) remains identical to the validated research baseline.

### Step 3: Build & Push
- Multi-stage Docker builds to minimize image size.
- Scan for hardcoded API keys/secrets.

---

## 3. Deployment Discipline
- **State**: Only `/data` and `/logs` are persistent. The system remains stateless otherwise.
- **Scaling**: Uvicorn workers scaled to CPU count.
- **Rate Limits**: SEC Rate compliance handled via global `SEC_REQUEST_RATE_LIMIT` in `config.py`.
