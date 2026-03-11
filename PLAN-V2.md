# Investment Opportunity Dashboard — Feature Expansion Plan

## Context

The dashboard currently shows sector-level YoY changes (treemap), sub-industry sparklines, and indicator time-series charts with date controls. While useful for monitoring, it doesn't answer the core question: **"Where are the investment opportunities right now?"**

This plan adds 8 features across 6 phases to transform the dashboard from a data viewer into an investment opportunity finder. The **Business Cycle Indicator** is the north star — everything else feeds into or extends it.

---

## Dashboard Layout (Final State)

```
┌─────────────────────────────────────────────────────┐
│  Header                                              │
├──────────────────────┬──────────────────────────────-┤
│  Cycle Clock         │  Leading Indicators Summary    │  ← Phase D
│  (polar chart)       │  + Sector Recommendations      │
├──────────────────────┴──────────────────────────────-┤
│  Executive Summary: traffic lights + narrative        │  ← Phase E
├─────────────────────────────────────────────────────-┤
│  Controls: country | date presets | YoY toggle        │
├─────────────────────────────────────────────────────-┤
│  Momentum Scoreboard (ranked horizontal bars)         │  ← Phase C
├─────────────────────────────────────────────────────-┤
│  Anomaly Alerts (collapsible)                         │  ← Phase B
├─────────────────────────────────────────────────────-┤
│  Tabs: [Sectors] [US vs Canada] [Correlations]        │  ← Phase F
│    └─ Treemap / sparkline table / indicator charts    │
│       └─ Percentile gauges at indicator level         │  ← Phase B
└─────────────────────────────────────────────────────-┘
```

---

## Phase A: Acceleration Infrastructure

> Foundation: acceleration math is reused by Momentum Scoreboard, Business Cycle, and Executive Summary.

### Backend
- [ ] **New**: `backend/app/services/acceleration_service.rb`
  - Takes an indicator, computes 3-month rate of change (first derivative)
  - Acceleration: change in 3M rate vs prior 3M rate (second derivative)
  - Direction label: "accelerating" / "decelerating" / "stable"
  - Reuses `data_points.order(:date)` pattern from `SectorSummaryService`
- [ ] **Modify**: `backend/config/routes.rb` — add `get :acceleration, on: :member` under indicators
- [ ] **Modify**: `backend/app/controllers/api/v1/indicators_controller.rb` — add `acceleration` action

### Frontend
- [ ] **Modify**: `frontend/api_client.py` — add `get_indicator_acceleration()`

### No UI changes in this phase

---

## Phase B: Percentile Gauges + Anomaly Detection

### B1: Percentile Service
- [ ] **New**: `backend/app/services/percentile_service.rb`
  - For each indicator in a country: current value's percentile within 5-year range
  - Returns: `{ indicator_id, name, sector_name, current, min, max, percentile, classification }`
  - Classifications: extreme_low (<5th), low (5-20th), normal (20-80th), high (80-95th), extreme_high (>95th)
- [ ] **New route**: `GET /api/v1/countries/:id/percentiles`
- [ ] **Frontend**: `build_percentile_gauge()` — `go.Indicator` with gauge mode, shown at indicator drill-down level

### B2: Anomaly Detection
- [ ] **New**: `backend/app/services/anomaly_detection_service.rb`
  - 12-month rolling mean + standard deviation per indicator
  - Flag indicators >2σ from rolling mean
  - Compute z-score for severity: "warning" (2-3σ) or "critical" (>3σ)
- [ ] **New route**: `GET /api/v1/countries/:id/anomalies`
- [ ] **Frontend**: `build_anomaly_panel()` — collapsible `dbc.Collapse` panel listing anomalies with severity badges
- [ ] **Frontend**: Anomaly badges on treemap tiles via customdata
- [ ] **Modify**: `frontend/layouts.py` — add anomaly panel container

---

## Phase C: Sector Momentum Scoreboard

- [ ] **New**: `backend/app/services/momentum_scoreboard_service.rb`
  - Composite score per sector (range -100 to +100):
    - 40% weight: YoY change (from existing `SectorSummaryService`)
    - 35% weight: 3-month rate of change (from `AccelerationService`)
    - 25% weight: trend direction (+1 up, 0 flat, -1 down)
  - Rank sectors 1-8, include previous month's rank for rank-change arrows
  - Include acceleration label per sector
- [ ] **New route**: `GET /api/v1/countries/:id/momentum`
- [ ] **Frontend**: `build_momentum_scoreboard()` in `components.py`
  - Vertical list of `dbc.Card` components sorted by rank
  - Horizontal bar showing composite score, colored by positive/negative
  - Acceleration arrow + YoY and 3M rate as secondary metrics
  - Positioned between controls and treemap (always visible when country selected)
- [ ] **Modify**: `frontend/layouts.py`, `frontend/callbacks.py`

---

## Phase D: Business Cycle Indicator (Core Feature)

### D1: Indicator Classifications
- [ ] **New**: `backend/config/indicator_classifications.yml`

```yaml
us:
  leading:
    - UMCSENT    # Consumer Sentiment
    - PERMIT     # Building Permits
    - ICSA       # Initial Jobless Claims (inverted)
    - DGORDER    # Durable Goods Orders
    - M2SL       # M2 Money Supply
    - BAA10Y     # BAA Spread (inverted)
    - HOUST      # Housing Starts
  coincident:
    - INDPRO     # Industrial Production
    - PAYEMS     # Nonfarm Payrolls
    - RSAFS      # Retail Sales
    - PCE        # Personal Consumption
  lagging:
    - UNRATE     # Unemployment Rate
    - CES0500000003  # Average Hourly Earnings
    - CPIAUCSL   # CPI
    - TOTALSL    # Consumer Credit
    - FEDFUNDS   # Fed Funds Rate
  inverted:      # Higher = worse for these
    - UNRATE
    - ICSA
    - BAA10Y
  sector_cycle_map:
    expansion: [Consumer, Financial, Energy]
    peak: [Energy, Inflation]
    contraction: [Financial, Trade]
    trough: [Housing, Manufacturing]
```

### D2: Composite Leading Index
- [ ] **New**: `backend/app/services/business_cycle_service.rb`
  - Algorithm (simplified Conference Board methodology):
    1. Select leading indicators from config
    2. Compute symmetric % change: `200 * (Vt - Vt-1) / (Vt + Vt-1)`
    3. Normalize by dividing by historical standard deviation
    4. Sum normalized changes → composite monthly change
    5. Cumulate into index (base = 100)
  - Cycle phase detection:
    - **Expansion**: Index rising AND above 12-month moving average
    - **Peak**: Was rising, now declining
    - **Contraction**: Index declining AND below 12-month MA
    - **Trough**: Was declining, now rising
  - Returns: `{ composite_index, current_phase, phase_duration_months, sector_recommendations, leading_indicators_summary }`
- [ ] **New route**: `GET /api/v1/countries/:id/business_cycle`

### D3: Frontend — Cycle Clock Hero
- [ ] **New component**: `build_cycle_clock()` — `go.Scatterpolar` with 4 quadrants
  - Dot marker at current phase, arc showing historical path
  - Phase label in large colored text (green/yellow/red/blue)
  - Duration: "X months in expansion"
- [ ] **New component**: `build_leading_summary()` — compact grid of 7 leading indicators with arrows
- [ ] **Modify**: `frontend/layouts.py` — insert `cycle-hero` div between header and controls (60/40 split)
- [ ] **Modify**: `frontend/assets/style.css` — cycle clock styles

---

## Phase E: Executive Summary Panel

- [ ] **New**: `backend/app/services/executive_summary_service.rb`
  - Calls cached results from Momentum, Anomaly, and BusinessCycle services
  - **Traffic lights**: Per sector — green (score >20 + accelerating), yellow (±20 or stable), red (<-20 + decelerating)
  - **Narrative bullets** (template-driven, ranked by significance):
    1. Cycle phase: "Economy in expansion for 14 months"
    2. Anomalies: "Housing Starts 2.3σ below rolling mean"
    3. Momentum extremes: "Manufacturing accelerating 3rd consecutive month, ranked #1"
    4. Percentile extremes: "Consumer Sentiment at 8th percentile of 5-year range"
    5. Divergences: "Leading indicators diverging from lagging — potential turning point"
- [ ] **New route**: `GET /api/v1/countries/:id/executive_summary`
- [ ] **Frontend**: `build_executive_summary()` — `dbc.Card` with traffic light grid (8 colored dots) + narrative `html.Li` bullets
- [ ] Position below cycle hero, above controls

---

## Phase F: Cross-Country Comparison + Correlation Heatmap

### F1: Cross-Country
- [ ] **New**: `backend/app/services/cross_country_service.rb`
  - Matches US & Canada sectors by name (same 8 names)
  - Side-by-side YoY, relative delta, trend direction per sector
- [ ] **New route**: `GET /api/v1/countries/:id/compare/:other_id`
- [ ] **Frontend**: `build_cross_country_comparison()` — butterfly/diverging `go.Bar` chart

### F2: Correlation Heatmap
- [ ] **New**: `backend/app/services/correlation_service.rb`
  - Pairwise Pearson correlation between indicators (align by date)
  - 12-month rolling correlation vs full-period → flag divergences >0.4 gap
  - Default: sector-level (8x8), expandable to indicator-level
- [ ] **New route**: `GET /api/v1/countries/:id/correlations`
- [ ] **Frontend**: `build_correlation_heatmap()` — `go.Heatmap` with clickable cells → dual-axis overlay chart
- [ ] **Modify**: `frontend/layouts.py` — add `dbc.Tabs` in drill-down zone: [Sectors] [US vs Canada] [Correlations]

---

## New Backend Services Summary

| Service | File | Cached | Depends On |
|---------|------|--------|------------|
| AccelerationService | `acceleration_service.rb` | No (fast) | — |
| PercentileService | `percentile_service.rb` | 1hr | — |
| AnomalyDetectionService | `anomaly_detection_service.rb` | 1hr | Percentile stats |
| MomentumScoreboardService | `momentum_scoreboard_service.rb` | 1hr | Acceleration |
| BusinessCycleService | `business_cycle_service.rb` | 1hr | Acceleration, YAML config |
| ExecutiveSummaryService | `executive_summary_service.rb` | 1hr | Momentum, Anomaly, Cycle |
| CrossCountryService | `cross_country_service.rb` | 1hr | SectorSummary |
| CorrelationService | `correlation_service.rb` | 1hr | — |

## New API Routes (7 endpoints + 1 indicator endpoint)

```ruby
resources :countries do
  get :business_cycle, on: :member
  get :momentum, on: :member
  get :executive_summary, on: :member
  get :anomalies, on: :member
  get :percentiles, on: :member
  get :correlations, on: :member
  get 'compare/:other_id', action: :compare, on: :member
end
resources :indicators do
  get :acceleration, on: :member
end
```

## Phase Dependencies

```
Phase A (Acceleration) → Phase C (Momentum) → Phase E (Executive Summary)
Phase B (Percentiles + Anomalies) ↗               ↑
                                   Phase D (Business Cycle) ↗
Phase F (Cross-Country + Correlations) — independent, after UI patterns from C-E
```

## Verification

After each phase:
1. `docker compose restart backend frontend`
2. Visit `http://localhost:8050`
3. **Phase A**: `curl http://localhost:8051/api/v1/indicators/1/acceleration` → returns rate_of_change, acceleration, direction
4. **Phase B**: `curl .../countries/1/anomalies` → flags with z-scores; percentile gauges visible at indicator level
5. **Phase C**: Momentum scoreboard visible below controls, sectors ranked with bars + arrows
6. **Phase D**: Cycle clock hero at top showing current phase, leading indicators summary, sector recommendations
7. **Phase E**: Traffic lights + narrative bullets auto-generated from data
8. **Phase F**: Tabs switch between Sectors/Comparison/Correlations; heatmap clickable for overlay charts
