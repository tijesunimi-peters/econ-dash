# Phase 3: Structural & Long-Term Trends - Implementation Progress

## Overview
Phase 3 adds long-term structural context to the dashboard:
- **Demographics**: Population aging, labor force participation
- **Debt metrics**: Government, corporate, household debt levels
- **Productivity**: Labor productivity growth, R&D spending, education investment

**Target**: Full implementation with sample data, API endpoints, and frontend panel

---

## Milestones

### ✅ Planning Complete
- [x] Architecture design (follow Phases 1 & 2 pattern)
- [x] Data model design (2 tables: structural_metrics, debt_metrics)
- [x] Component design (3-section layout: demographics, debt, productivity)
- [x] Verification strategy (migration → API → frontend integration)

### 📋 Implementation Tasks

#### Backend: Models (Estimated: 1-2 hours)
- [ ] Create `backend/app/models/structural_metric.rb` (60-80 lines)
  - Model, constants (7 metric types), validations, scopes, instance methods
- [ ] Create `backend/app/models/debt_metric.rb` (60-80 lines)
  - Model, constants (4 metric types), validations, scopes, instance methods
- [ ] Modify `backend/app/models/country.rb` (2 lines)
  - Add `has_many :structural_metrics`, `has_many :debt_metrics`

#### Backend: Database (Estimated: 30 mins)
- [ ] Create migration: `create_structural_metrics` (15 lines + 3 indexes)
- [ ] Create migration: `create_debt_metrics` (15 lines + 3 indexes)
- [ ] Run migrations: `db:migrate`

#### Backend: API (Estimated: 1 hour)
- [ ] Modify `backend/config/routes.rb` (2 lines)
  - Add `:structural_trends` and `:debt_trends` member routes
- [ ] Modify `backend/app/controllers/api/v1/countries_controller.rb` (40 lines)
  - Add `structural_trends` action (groups by metric_type, returns latest-per-metric)
  - Add `debt_trends` action (groups by metric_type, returns latest-per-metric)
- [ ] Test endpoints via curl

#### Backend: Seed Data (Estimated: 1-2 hours)
- [ ] Create `backend/db/seeds/structural_metrics.rb` (40 lines)
  - 7 metrics × 5 countries = 35 records
- [ ] Create `backend/db/seeds/debt_metrics.rb` (40 lines)
  - 4 metrics × 5 countries = 20 records
- [ ] Modify `backend/db/seeds.rb` (2 lines)
  - Add require statements
- [ ] Run `db:seed` and verify count: StructuralMetric.count=35, DebtMetric.count=20

#### Frontend: API Client (Estimated: 15 mins)
- [ ] Modify `frontend/api_client.py` (4 lines)
  - Add `get_country_structural_trends(country_id)`
  - Add `get_country_debt_trends(country_id)`

#### Frontend: Components (Estimated: 2-3 hours)
- [ ] Modify `frontend/components.py` (200 lines)
  - Create `build_structural_health(structural_data, debt_data)` function
  - Build 3 sections: demographics, debt, productivity
  - Implement card styling with alert color logic
  - Guard clauses, error handling

#### Frontend: Integration (Estimated: 1 hour)
- [ ] Modify `frontend/layouts.py` (1 line)
  - Add `html.Div(id="structural-panel-container")`
- [ ] Modify `frontend/callbacks.py` (20 lines)
  - Create `update_structural_panel(nav)` callback
  - Fetch both API endpoints, guard clauses, error handling
- [ ] Modify `frontend/assets/style.css` (40 lines)
  - `.structural-panel`, `.structural-grid`, `.structural-section`, `.structural-metric-card`

#### Testing & Verification (Estimated: 1 hour)
- [ ] Run migrations and verify tables
- [ ] Load seed data and verify counts
- [ ] Test `/api/v1/countries/1/structural_trends` endpoint
- [ ] Test `/api/v1/countries/1/debt_trends` endpoint
- [ ] Restart frontend and verify panel renders
- [ ] Switch countries and verify data updates
- [ ] Test responsive layout (mobile view)
- [ ] Check browser console for errors

---

## Key Files

### Backend
- `backend/app/models/structural_metric.rb` (CREATE)
- `backend/app/models/debt_metric.rb` (CREATE)
- `backend/app/models/country.rb` (MODIFY: +2 lines)
- `backend/config/routes.rb` (MODIFY: +2 lines)
- `backend/app/controllers/api/v1/countries_controller.rb` (MODIFY: +40 lines)
- `backend/db/migrate/TIMESTAMP_create_structural_metrics.rb` (CREATE)
- `backend/db/migrate/TIMESTAMP_create_debt_metrics.rb` (CREATE)
- `backend/db/seeds/structural_metrics.rb` (CREATE)
- `backend/db/seeds/debt_metrics.rb` (CREATE)
- `backend/db/seeds.rb` (MODIFY: +2 lines)

### Frontend
- `frontend/api_client.py` (MODIFY: +4 lines)
- `frontend/components.py` (MODIFY: +200 lines)
- `frontend/layouts.py` (MODIFY: +1 line)
- `frontend/callbacks.py` (MODIFY: +20 lines)
- `frontend/assets/style.css` (MODIFY: +40 lines)

---

## Data Model

### StructuralMetric
```
- id (PK)
- country_id (FK)
- metric_type: population | median_age | labor_participation | life_expectancy | tfp_growth | rd_pct_gdp | education_spending
- value (decimal)
- date
- unit: % | years | millions | billions
- source
- alert_level (computed): 'normal' | 'warning' | 'critical'
```

### DebtMetric
```
- id (PK)
- country_id (FK)
- metric_type: govt_debt_pct_gdp | corp_debt_ratio | hhd_debt_pct_income | deficit_pct_gdp
- value (decimal)
- date
- unit
- source
- trend: up | down | stable
- alert_level (computed): 'normal' | 'warning' | 'critical'
```

---

## Alert Thresholds (Hardcoded for MVP)

### Demographics
- Median age: Warning >45, Critical >50
- Labor participation: Warning <60%, Critical <55%
- Population growth: Warning <0.5%, Critical <0%
- Life expectancy: No alert (trend only)

### Debt
- Govt debt % GDP: Warning >80%, Critical >100%
- Corporate debt ratio: Warning >2.5, Critical >3.0
- Household debt % income: Warning >90%, Critical >110%
- Budget deficit % GDP: Warning >3%, Critical >5%

### Productivity
- Labor productivity growth: Warning <1%, Critical <0%
- R&D as % GDP: Warning <1.5%, Critical <1.0%
- Education spending % GDP: Warning <4%, Critical <3%

---

## Sample Data (5 countries × 11 metrics = 55 records)

### Countries & Their Profiles
- **US**: Strong productivity, moderate debt, aging (>40)
- **CA**: Similar to US, energy-dependent
- **JP**: Severe aging (>48), low growth, high debt
- **AU**: Young (38), high debt, commodity-dependent
- **DE**: Moderate aging, strict fiscal rules, energy transition

---

## Success Criteria

- [x] Plan documented in PHASE3_PROGRESS.md
- [ ] All 2 models created with proper validations & scopes
- [ ] 2 migrations run successfully
- [ ] ~55 seed records loaded
- [ ] 2 API endpoints return proper JSON responses
- [ ] Frontend component renders all 3 sections (demographics, debt, productivity)
- [ ] Alert colors display correctly based on thresholds
- [ ] Panel updates when country changes
- [ ] No console errors
- [ ] Responsive layout works on mobile

---

## Notes

- **No FRED API needed** for Phase 3 MVP — seed data only
- **Alert thresholds are hardcoded** in model instance methods for speed
- **Component follows Phase 2 styling** (sentiment-card pattern) to minimize CSS
- **Same callback architecture** as Phases 1 & 2 for consistency
- **Future: Move thresholds to ConfigMetric table** for runtime adjustability

---

## Timeline Estimate

**Total: 6-8 hours** (spread across multiple sessions)
- Backend models & DB: 2-3 hours
- Backend API & routes: 1 hour
- Seed data: 1-2 hours
- Frontend: 2-3 hours
- Testing & verification: 1 hour

**Ready to start**: Backend models first
