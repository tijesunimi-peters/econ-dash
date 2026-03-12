# Economic Dashboard API Reference

All endpoints are under `/api/v1/` and return JSON.

## Countries

### List Countries
**GET** `/countries`

Returns all countries with basic info (id, name, code).

```json
[
  { "id": 1, "name": "United States", "code": "US" },
  { "id": 2, "name": "Canada", "code": "CA" }
]
```

### Get Country Details
**GET** `/countries/:id`

Returns country with list of sectors.

```json
{
  "id": 1,
  "name": "United States",
  "code": "US",
  "sectors": [
    { "id": 1, "name": "Manufacturing", "description": "..." }
  ]
}
```

### Country Business Cycle Analysis
**GET** `/countries/:id/business_cycle`

Detects current business cycle phase (expansion, peak, contraction, trough) using leading indicators with 12-month moving average.

**Response:**
```json
{
  "composite_index": [
    { "date": "2025-09-01", "value": 102.45 },
    { "date": "2025-10-01", "value": 103.12 }
  ],
  "current_phase": "expansion",
  "phase_duration_months": 8,
  "cycle_position": {
    "phase": "expansion",
    "quadrant": "expansion",
    "quadrant_label": "Expansion",
    "x_position": 0.725,     // 0=at trend, 1=well above trend
    "y_position": 0.823,     // 0=declining momentum, 1=accelerating
    "momentum": 3.142,       // Positive=accelerating, negative=decelerating
    "roc_1m": 0.68,          // 1-month rate of change %
    "roc_3m": 2.14,          // 3-month rate of change %
    "roc_6m": 4.33,          // 6-month rate of change %
    "current_vs_ma": 3.82    // % above/below 12-month MA
  },
  "sector_recommendations": ["Manufacturing", "Consumer"],
  "leading_indicators_summary": [
    {
      "name": "Initial Jobless Claims",
      "source_series_id": "ICSA",
      "current_value": 215000,
      "direction": "down",
      "rate_of_change": -2.3,
      "inverted": true
    }
  ]
}
```

**Cache:** 1 hour

### Business Cycle Percentiles
**GET** `/countries/:id/percentiles`

Returns percentile positions of key indicators relative to historical distribution.

**Cache:** 1 hour

### Anomalies Detection
**GET** `/countries/:id/anomalies`

Identifies unusual movements in indicators (>1.5 std dev from 3-year mean).

**Cache:** 1 hour

### Momentum Scoreboard
**GET** `/countries/:id/momentum`

Rates momentum (rate of change) across sectors and sub-industries on 0-100 scale.

**Cache:** 1 hour

### Executive Summary
**GET** `/countries/:id/executive_summary`

High-level narrative summary of country's economic condition.

**Cache:** 1 hour

### Sector Correlations
**GET** `/countries/:id/correlations`

Computes rolling 12-month Pearson correlations between sectors to identify co-movements.

**Cache:** 1 hour

### Compare Countries
**GET** `/countries/:id/compare/:other_id`

Side-by-side comparison of two countries across key metrics.

**Cache:** 1 hour

### Countries by Cycle Phase
**GET** `/countries/by_cycle_phase/:phase`

Filter countries by business cycle phase.

**Parameters:**
- `phase` (required) — One of: `expansion`, `peak`, `contraction`, `trough`

**Response:**
```json
{
  "phase": "expansion",
  "countries": [
    {
      "id": 1,
      "name": "United States",
      "code": "US",
      "phase": "expansion",
      "duration_months": 8,
      "cycle_position": { /* as above */ },
      "sector_recommendations": ["Manufacturing", "Consumer"]
    }
  ],
  "count": 1
}
```

**Errors:**
- `400 Bad Request` — Invalid phase. Valid phases: expansion, peak, contraction, trough

### Causal Factors
**GET** `/countries/:id/causal_factors`

Explains *why* trends are happening through external and structural dependencies (oil prices, export concentration, FX linkages, etc).

**Response:**
```json
{
  "factors": [
    {
      "id": "us_oil_wti",
      "name": "WTI Crude Oil",
      "description": "Domestic energy production and consumption",
      "type": "commodity_price",
      "current_proxy_value": 78.45,
      "proxy_status": "rising",
      "pct_change_3m": 8.2,
      "correlation_with_sector": 0.68,
      "affected_sectors": ["Energy", "Inflation", "Consumer"],
      "sensitivity": "high",
      "confidence": 0.81,
      "rank": 1
    }
  ]
}
```

**Cache:** 1 hour

### Country Summary
**GET** `/countries/:id/summary`

Returns sector summaries and composite data.

**Cache:** 1 hour

---

## Sectors

### Get Sector Details
**GET** `/sectors/:id`

Returns sector with list of sub-industries.

```json
{
  "id": 1,
  "name": "Manufacturing",
  "description": "...",
  "sub_industries": [
    { "id": 1, "name": "Durable Goods", "description": "..." }
  ]
}
```

### Sector Summary
**GET** `/sectors/:id/summary`

Summary metrics for a sector.

**Cache:** 1 hour

---

## Sub-Industries

### Get Sub-Industry Details
**GET** `/sub_industries/:id`

Returns sub-industry with list of indicators.

```json
{
  "id": 1,
  "name": "Durable Goods",
  "description": "...",
  "indicators": [
    { "id": 1, "name": "New Orders", "description": "..." }
  ]
}
```

---

## Indicators

### Get Indicator Details
**GET** `/indicators/:id`

Returns indicator metadata.

```json
{
  "id": 1,
  "name": "Industrial Production Index",
  "description": "...",
  "source_series_id": "INDPRO",
  "frequency": "monthly"
}
```

### Indicator Time Series
**GET** `/indicators/:id/series`

Returns historical data points for an indicator.

```json
{
  "id": 1,
  "name": "Industrial Production Index",
  "data": [
    { "date": "2020-01-01", "value": 102.3 },
    { "date": "2020-02-01", "value": 102.8 }
  ]
}
```

### Indicator Acceleration
**GET** `/indicators/:id/acceleration`

Analyzes rate of change and acceleration/deceleration trends.

```json
{
  "id": 1,
  "name": "Industrial Production Index",
  "direction": "up",
  "pct_change_1m": 0.5,
  "pct_change_3m": 1.2,
  "pct_change_6m": 2.8,
  "acceleration": "accelerating"
}
```

---

## Error Responses

All errors return JSON with status code and message:

```json
{
  "error": "Country not found"
}
```

**Common Status Codes:**
- `200 OK` — Success
- `400 Bad Request` — Invalid parameters
- `404 Not Found` — Resource not found
- `500 Internal Server Error` — Server error

---

## Caching

Expensive endpoints are cached for **1 hour**:
- `/business_cycle`
- `/percentiles`
- `/anomalies`
- `/momentum`
- `/executive_summary`
- `/correlations`
- `/compare/:other_id`
- `/causal_factors`
- `/summary`
- Sector `/summary`

To invalidate cache: `curl -X POST http://localhost:8051/rails/cache/clear`
