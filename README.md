# Financial Narrative Drift Detection System
![CI Status](https://github.com/yourusername/fin-drift-engine/actions/workflows/ci.yml/badge.svg)

A professional, research-grade quantitative analytical instrument designed to detect structural divergence between corporate narrative and objective financial performance.

## 🏛️ System Architecture

```mermaid
graph TD
    subgraph "Ingestion & Data Flow"
        SEC[SEC Edgar API] -->|XBRL JSON| Ingest[src/ingestion.py]
        Ingest -->|Raw JSON Cache| RawDir[/data/raw/]
    end

    subgraph "Analytical Core"
        RawDir --> Norm[src/normalization.py]
        Norm -->|Canonical CSV| ProcDir[/data/processed/]
        ProcDir --> Feat[src/features.py]
        Feat -->|Financial Metrics| Drift[src/drift.py]
        ProcDir --> Nar[src/narrative.py]
        Nar -->|Sentiment Signals| Drift
    end

    subgraph "Orchestration & Output"
        Pipe[src/pipeline.py] -->|Coordinates| Analytics
        Drift --> Result["outputs/{ticker}/{date}/"]
        Result --> Viz[src/visualization.py]
        Result --> Report[src/reporting.py]
    end
```

## 🚀 Deployment & Operations

### 1. Persistent Environment (Docker)
The recommended way to run the engine is via Docker to ensure environment determinism.

```bash
# Clone and build
docker build -t drift-engine .

# Run analysis for specific tickers
docker run --env-file .env -v $(pwd)/outputs:/app/outputs drift-engine --tickers NVDA MSFT
```

### 2. Manual CLI Setup
```bash
pip install .
python main.py --tickers AAPL --start_year 2022
```

### 3. Environment Configuration
Create a `.env` file based on `.env.example`:
- `SEC_USER_AGENT`: Required for SEC API access ("Name (email)")
- `OPENAI_API_KEY`: Required for narrative sentiment extraction
- `LOG_LEVEL`: defaults to `INFO`

## 📊 Analytical Methodology

### Drift Score Calculation
Structural divergence is measured by the delta between Narrative Momentum ($M_{nar}$) and Financial Momentum ($M_{fin}$):

$$D = M_{nar} - M_{fin}$$

Where:
- $M_{fin}$ is a weighted vector of Revenue Growth, OCF Growth, and Accrual Quality.
- $M_{nar}$ is a weighted vector of Optimism and Risk trajectory.

## 📁 Storage Discipline & Observability
- **`/data/`**: Tiered storage for raw and processed analytical artifacts.
- **`/outputs/`**: Versioned historical results (`{ticker}/{YYYYMMDD}/`).
- **`/logs/`**: Structured observability via `pipeline.log`.

## 🧪 Testing & Validation
Unit and integration tests are strictly enforced via the CI pipeline.
```bash
python -m unittest discover tests
```
