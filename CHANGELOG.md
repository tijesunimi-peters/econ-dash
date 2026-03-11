# Changelog

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
