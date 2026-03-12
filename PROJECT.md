# Economic Health Dashboard

## Goal

A multi-country (US, Canada, Japan, Australia, Germany) economic monitoring dashboard that provides a hierarchical view of economic health across sectors and industries. The dashboard enables users to:

1. **See sector-level trends at a glance** — quickly identify which sectors of the economy are expanding or contracting
2. **Drill down into sub-industries** — understand what's driving a sector's performance by examining its constituent industries
3. **Analyze contributing indicators** — view the underlying time-series data (GDP, employment, production, prices) that explain sub-industry trends
4. **Understand causal factors** — discover external and structural dependencies driving trends (e.g., oil prices, currency movements, trade concentration)
5. **Compare countries side-by-side** — monitor multiple economies with consistent sector categorization

## Architecture

- **Backend**: Rails 8.1 API (PostgreSQL) — data ingestion, storage, and REST API
- **Frontend**: Plotly Dash — interactive drill-down visualizations
- **Data Sources**: FRED API (US + most Canadian series), Bank of Canada Valet API
- **Infrastructure**: Docker Compose (3 services: db, backend, frontend)

## Data Hierarchy

```
Country (US, Canada)
  └── Sector (Manufacturing, Labour, Housing, Consumer, Financial, Energy, Inflation, Trade)
        └── Sub-Industry (e.g., Durable Goods, Employment, Construction)
              └── Indicator (e.g., Unemployment Rate, CPI, Housing Starts)
                    └── DataPoint (date + value, ~5 years of history)
```

## Ports

| Service    | Host Port | Container Port |
|------------|-----------|----------------|
| PostgreSQL | 6543      | 5432           |
| Rails API  | 8051      | 3000           |
| Dash UI    | 8050      | 8050           |

## Running

```bash
cd /home/admin/econ-dashboard
docker compose up -d
docker compose exec backend bin/rails db:create db:migrate db:seed
docker compose exec backend bin/rails data:ingest
```

**Access dashboard at:** http://localhost:8050

## Documentation

- **[STATUS.md](STATUS.md)** — Current project status, completed features, architecture overview, testing checklist
- **[API_ENDPOINTS.md](API_ENDPOINTS.md)** — Full REST API reference with examples, parameters, caching policies
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** — Development workflow, common tasks, debugging, troubleshooting
- **[CHANGELOG.md](CHANGELOG.md)** — Version history and feature releases
- **[PLAN-CAUSAL-FACTORS.md](PLAN-CAUSAL-FACTORS.md)** — Design document for causal factors feature
- **[PLAN-COUNTRIES.md](PLAN-COUNTRIES.md)** — Design document for adding Japan, Australia, Germany

## Features Implemented

### ✅ Multi-Country Support
- 5 countries: US, CA, JP, AU, DE
- Consistent sector taxonomy across countries
- 8,883+ economic data points from FRED API

### ✅ Business Cycle Analysis
- Composite leading index with 12-month moving average
- 4-phase detection: expansion, peak, contraction, trough
- 2D cycle positioning with momentum scoring
- Sector recommendations per phase

### ✅ Anomaly Detection
- Statistical detection (>1.5 std dev from 3-year mean)
- Visual flagging in dashboard

### ✅ Causal Factors
- 13 factors across 5 countries
- Rolling 12-month Pearson correlation analysis
- Proxy series trend detection
- Confidence scoring and ranking

### ✅ Cross-Country Analysis
- Side-by-side comparison charts
- Sector correlation heatmap (rolling 12-month)
- Cycle phase filtering endpoint

### ✅ Advanced Analytics
- Momentum scoreboard with rate-of-change metrics
- Executive summaries with trend narratives
- Percentile analysis
- Acceleration detection

### ✅ Interactive Dashboard
- Country selector dropdown
- Drill-down from sector → sub-industry → indicator
- Time-series charts with Plotly
- Multiple tabs: Sectors, Momentum, Compare, Intelligence
