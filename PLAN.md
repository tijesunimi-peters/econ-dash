# UX Upgrade Plan — Implementation Tracker

## Overview

Upgrade the dashboard from plain text cards + basic line charts to an interactive treemap + sparkline table + contextual time-series with proper navigation.

---

## Phase 1: Backend Summary Endpoints
> All frontend improvements depend on these computed metrics.

- [x] **1A.** Create `SectorSummaryService` — computes per-sector YoY change, trend direction
  - File: `backend/app/services/sector_summary_service.rb`
- [x] **1B.** Create `SubIndustrySummaryService` — per-sub-industry metrics + 12-month sparkline data
  - File: `backend/app/services/sub_industry_summary_service.rb`
- [x] **1C.** Add API endpoints — `GET /countries/:id/summary`, `GET /sectors/:id/summary`
  - Files: `backend/config/routes.rb`, `countries_controller.rb`, `sectors_controller.rb`
- [x] **1D.** Cache responses (1 hour TTL via Rails.cache.fetch)

## Phase 2: Frontend Restructure + Treemap + Breadcrumbs
> Depends on Phase 1.

- [x] **2A.** Split `app.py` into modules: `layouts.py`, `callbacks.py`, `components.py`, `styles.py`
- [x] **2B.** Add `dash-bootstrap-components` to requirements.txt
- [x] **2C.** Extend `api_client.py` with `get_country_summary`, `get_sector_summary`
- [x] **2D.** Build treemap component (color = YoY %, click to drill down)
  - File: `frontend/components.py`
- [x] **2E.** Build breadcrumb navigation (always visible, clickable to jump back)
- [x] **2F.** Rewrite callbacks for state-driven navigation via `nav-state` Store
  - File: `frontend/callbacks.py`
- [x] **2G.** Build layout with dbc grid, breadcrumb slot, loading wrapper
  - File: `frontend/layouts.py`

## Phase 3: Sparkline Table + Date Controls + YoY Toggle
> Depends on Phase 2.

- [x] **3A.** Sparkline table for sub-industries (name, latest, YoY change, mini chart)
- [x] **3B.** Date range preset buttons (YTD, 1Y, 2Y, 5Y) wired to `date-range-store`
- [x] **3C.** YoY toggle switch on indicator charts (client-side pct_change transform)

## Phase 4: Polish
> Phase 4C/4D can run parallel with Phase 3.

- [x] **4A.** Loading states (`dcc.Loading` wrapper)
- [x] **4B.** Error handling in `api_client.py` (try/except, `dbc.Alert` on failure)
- [x] **4C.** Chart improvements (recession shading, unified hover, consistent template)
- [x] **4D.** External CSS (`frontend/assets/style.css`, remove inline CSS)

---

## Key Design Decisions

1. **Compute metrics in Ruby, not SQL** — dataset is small (~7,500 points), simpler to maintain
2. **Equal-sized treemap tiles** — no GDP weighting data available yet
3. **State-driven navigation** — single `dcc.Store` drives all views, replaces style toggling
4. **`dash-bootstrap-components`** — provides grid, breadcrumbs, tables, spinners out of the box (FLATLY theme)
5. **Sparklines via mini `dcc.Graph`** in `dbc.Table` rows — keeps dependencies minimal

## Files Summary

### New Files
| File | Phase | Purpose |
|---|---|---|
| `backend/app/services/sector_summary_service.rb` | 1A | Sector-level metric computation |
| `backend/app/services/sub_industry_summary_service.rb` | 1B | Sub-industry metrics + sparkline data |
| `frontend/layouts.py` | 2G | Layout builder |
| `frontend/callbacks.py` | 2F | All callback definitions |
| `frontend/components.py` | 2D | Treemap, sparkline table, breadcrumb, date controls |
| `frontend/styles.py` | 2A | CSS constants, chart template |
| `frontend/assets/style.css` | 4D | External stylesheet |

### Modified Files
| File | Phase | Change |
|---|---|---|
| `backend/config/routes.rb` | 1C | Add summary routes |
| `backend/app/controllers/api/v1/countries_controller.rb` | 1C | Add summary action |
| `backend/app/controllers/api/v1/sectors_controller.rb` | 1C | Add summary action |
| `frontend/app.py` | 2A | Slim to init + registration |
| `frontend/api_client.py` | 2C, 4B | New endpoints + error handling |
| `frontend/requirements.txt` | 2B | Add dash-bootstrap-components |
