# Changelog

## 2026-03-12 — Causal Factors Feature

### Added
- **Causal Factors** — Explain *why* economic trends are happening through external and structural dependencies
  - Backend service `CausalFactorService` with rolling 12-month Pearson correlation analysis
  - Config-driven factor definitions in `backend/config/causal_factors.yml`
    - 13 factors across 5 countries (US, CA, JP, AU, DE)
    - Examples: Oil price dependencies, China export concentration, FX linkages, trade policies
  - New API endpoint: `GET /api/v1/countries/:id/causal_factors` (1-hour cache)
  - Factors computed with:
    - Proxy series correlation with affected sectors
    - Trend detection (rising/falling/stable)
    - Confidence scoring (correlation × proxy activity)
    - Automatic ranking by confidence
  - Frontend integration:
    - New `_build_factors_compact()` component for rendering factor chips
    - Color-coded by confidence (green≥0.7, yellow≥0.5, red<0.5)
    - Status emojis (📈 rising, 📉 falling, ➡️ stable)
    - Correlation scores and affected sector tags
    - Integrated into Intelligence Panel (after narrative bullets)
  - Graceful error handling for missing/insufficient data

### Fixed
- Updated `.env` for correct Docker PostgreSQL connection string

## 2026-03-11 — Initial Setup

### Added
- Rails 8.1 API backend with PostgreSQL
  - Models: Country, Sector, SubIndustry, Indicator, DataPoint
  - REST API under `/api/v1/` with endpoints for countries, sectors, sub-industries, indicators, and time-series data
  - CORS configured for Dash frontend origin
  - Data ingestion clients: FredClient, StatcanClient, BankOfCanadaClient
  - `IngestDataJob` for background data pulls
  - `data:ingest` rake task with retry logic and rate limiting
  - Recurring job scheduled daily at 6am (via solid_queue)
- Plotly Dash frontend
  - Country selector dropdown
  - Sector cards with click-to-drill-down into sub-industries
  - Sub-industry cards with click-to-drill-down into indicator time-series charts
  - Inline CSS styling
- Docker Compose setup
  - PostgreSQL 16, Rails (development Dockerfile), Dash
  - Health checks, volume mounts, environment files
  - Container names: `econ-dashboard-backend`, `econ-dashboard-frontend`
- Seed data: 2 countries, 8 sectors each (16 total), 32 sub-industries, 48 indicators
  - US: all indicators sourced from FRED
  - Canada: mostly FRED, Bank of Canada for overnight rate
- Environment files (`.env`) for both backend and frontend
- 5 years of historical data ingested (~7,500 data points)

### Fixed
- Added `libyaml-dev` and `pkg-config` to backend Dockerfile for psych gem
- Added `require "net/http"` to service clients
- Added `backend` to Rails allowed hosts for Docker networking
- Replaced 4 discontinued Canadian FRED series:
  - `CANRGDPMANQISMEI` → `PRMNTO01CAQ657S` (Manufacturing Production Index)
  - `CANHOUST` → `WSCNDW01CAQ489S` (Housing Starts)
  - `CARSLM` → `CANSLRTTO01GPSAM` (Retail Trade Volume)
  - `CANRGDPMINQISMEI` → `COCANZ21` (Mining & Oil Import Price Index)
