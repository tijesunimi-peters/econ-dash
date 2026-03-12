# Changelog

## 2026-03-12 (Session 6) — Phase 4: Trade Flows & Supply Chain ✅

### Added
- **Phase 4: Trade Flows & Supply Chain** — Complete strategic context layer
  - 7 trade flow types: exports, imports, trade balance, FDI, supply chain concentration, export diversification, import dependency ratio
  - Backend models: `TradeFlow` and `TradeFlowDataPoint` (mirrors Phase 3 pattern)
  - Database migrations: `create_trade_flows`, `create_trade_flow_data_points` with proper indexes
  - API endpoint: `GET /api/v1/countries/:id/trade_flows` (grouped by category)
  - Rake task: `trade_data:ingest` (fetches from World Bank, falls back to seed data)
  - Seed data: 35 records (7 metrics × 5 countries) with realistic values
  - Alert logic: Supply chain concentration (>40 critical, 30-40 warning), import dependency (>2.0 critical, 1.5-2.0 warning)
  - Frontend component: `build_trade_flows()` with 4 sections (balance, flows, investment, supply chain)
  - Callback: `update_trade_flows()` triggered on nav-state changes
  - CSS classes: `.trade-panel`, `.trade-grid`, `.trade-card` with hover effects
  - Value formatting: % for GDP metrics, ratio/index for supply chain metrics
  - Data source attribution: FRED, World Bank, or Seed Data

### Updated Documentation
- **INDEX.md** — Phase 4 completion noted, roadmap links updated
- **STATUS.md** — Phase 4 features added, architecture updated with new models
- **PROJECT.md** — Phase 4 description added, documentation links consolidated
- **ROADMAP.md** — New file with next steps, quick wins, and future features (Tiers 2-4)

### Fixed
- Data source labels: Trade flows correctly attributed (FRED vs World Bank)
- Seed data labeling: Structural metrics corrected to show FRED source

## 2026-03-12 (Session 5 continued) — API Documentation & Cycle Phase Filtering

### Added
- **Cycle Phase Filtering API** — `GET /api/v1/countries/by_cycle_phase/:phase`
  - Filter countries by business cycle phase (expansion, peak, contraction, trough)
  - Returns countries with cycle position data and sector recommendations
  - Enable cross-country cycle synchronization analysis
- **Comprehensive API Documentation** — `API_ENDPOINTS.md`
  - Full reference for all 20+ REST endpoints
  - Request/response examples for each endpoint
  - Parameter documentation and error handling
  - Caching policies (1-hour cache for expensive operations)
- **Project Memory** — Persistent notes on architecture, patterns, and debugging insights

### Fixed
- Committed `by_cycle_phase` controller action and collection route

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
