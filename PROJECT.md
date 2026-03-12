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
docker compose up --build
docker exec econ-dashboard-backend bin/rails db:create db:migrate db:seed
docker exec econ-dashboard-backend bin/rails data:ingest
```
