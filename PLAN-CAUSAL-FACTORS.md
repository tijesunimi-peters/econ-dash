# Add Causal Factors to Economic Dashboard

## Context
The dashboard currently displays economic indicators (business cycle, momentum, anomalies) but doesn't explain *why* trends are happening. Users need to understand external and structural factors driving economic changes—e.g., oil price spikes affecting CPI, China demand affecting exports, geopolitical disruptions.

This feature adds **quantified causal factors** by:
1. **Structural/geopolitical knowledge** (curated YAML config): Country-specific dependencies (energy import reliance, export concentration, currency dynamics)
2. **Quantitative correlation analysis**: Compute rolling correlations between proxy series and country indicators to detect active causal links
3. **UI integration**: Display top 5 factors in intelligence panel with impact scores, correlation strength, and affected sectors

## High-Level Design

### Architecture Layers

**Backend:**
- `config/causal_factors.yml` — Country + sector → factor definitions with proxy series IDs, descriptions, sensitivity levels
- `CausalFactorService` — Main orchestrator service
  - Load config
  - For each factor: fetch proxy series, compute rolling correlation (12-month window) with sector indicators
  - Rank by correlation strength and current status (proxy trending)
  - Return top 5 with detailed metadata
- `CountriesController#causal_factors` — New API endpoint (cached 1 hour)
- Routes: `GET /api/v1/countries/:id/causal_factors`

**Frontend:**
- `api_client.py` — New function `get_country_causal_factors(country_id)`
- `components.py` — New helper `_build_factors_compact()` to render factor chips in intelligence panel
- `callbacks.py` — Extend `update_intelligence_panel()` callback to fetch and pass causal factors data
- `layouts.py` — Already has the intelligence panel container; no layout changes needed
- `style.css` — Add `.factors-*` CSS for compact factor chips

### Data Model (Config-Driven, No DB Changes)

**causal_factors.yml structure:**
```yaml
jp:
  sectors:
    Energy:
      factors:
        - id: jp_oil_strait_hormuz
          name: "Strait of Hormuz Oil Exposure"
          description: "~90% of Japan's crude oil imports transit the Strait"
          type: external_dependency
          proxy_series_id: DCOILBRENTEU
          sensitivity: high
          affected_sectors: ["Energy", "Manufacturing", "Inflation"]
          lag_months: 2
    Trade:
      factors:
        - id: jp_china_demand
          name: "China Demand"
          description: "China is Japan's largest trading partner"
          type: export_concentration
          proxy_series_id: XTEXVA01CNM667S
          sensitivity: high
          affected_sectors: ["Manufacturing", "Trade", "Consumer"]

au:
  sectors:
    Trade:
      factors:
        - id: au_china_concentration
          name: "China Export Concentration"
          description: "~35% of Australia's exports go to China"
          type: export_concentration
          proxy_series_id: XTEXVA01CNM667S
          sensitivity: high
          affected_sectors: ["Trade", "Energy", "Manufacturing"]
    Energy:
      factors:
        - id: au_lng_export
          name: "LNG Export Prices"
          description: "LNG is a major export commodity"
          type: commodity_export
          proxy_series_id: DHHNGSP
          sensitivity: medium
          affected_sectors: ["Energy", "Trade"]

de:
  sectors:
    Energy:
      factors:
        - id: de_energy_import
          name: "Energy Import Dependency"
          description: "Germany imports >60% of energy"
          type: external_dependency
          proxy_series_id: DCOILBRENTEU
          sensitivity: high
          affected_sectors: ["Energy", "Manufacturing", "Inflation"]
    Manufacturing:
      factors:
        - id: de_china_demand
          name: "China Industrial Demand"
          type: export_concentration
          proxy_series_id: XTEXVA01CNM667S
          sensitivity: high
          affected_sectors: ["Manufacturing", "Financial"]
    Financial:
      factors:
        - id: de_usd_eur
          name: "USD/EUR Exchange Rate"
          description: "EUR weakness increases export competitiveness"
          type: financial_linkage
          proxy_series_id: DEXUSEU
          sensitivity: medium
          affected_sectors: ["Manufacturing", "Trade"]

us:
  sectors:
    Energy:
      factors:
        - id: us_oil_wti
          name: "WTI Crude Oil"
          description: "Domestic energy production and consumption"
          type: commodity_price
          proxy_series_id: DCOILWTICO
          sensitivity: high
          affected_sectors: ["Energy", "Inflation", "Consumer"]
    Manufacturing:
      factors:
        - id: us_china_tariffs
          name: "China Trade Relations"
          description: "Tariff impacts on manufacturing input costs"
          type: trade_policy
          proxy_series_id: XTEXVA01USM667S
          sensitivity: high
          affected_sectors: ["Manufacturing", "Consumer", "Financial"]

ca:
  sectors:
    Energy:
      factors:
        - id: ca_oil_usd
          name: "USD Commodity Strength"
          description: "Strengthening USD lowers oil prices in CAD terms"
          type: financial_linkage
          proxy_series_id: DCOILWTICO
          sensitivity: high
          affected_sectors: ["Energy", "Trade"]
    Trade:
      factors:
        - id: ca_us_demand
          name: "US Economic Activity"
          description: "~75% of Canadian exports go to US"
          type: export_concentration
          proxy_series_id: INDPRO
          sensitivity: high
          affected_sectors: ["Trade", "Manufacturing", "Energy"]
```

## Files to Create/Modify

### 1. Backend Config
**Create:** `backend/config/causal_factors.yml`
- Copy structure above
- Per-country, per-sector factor definitions
- Each factor has: id, name, description, type, proxy_series_id, sensitivity, affected_sectors, lag_months (optional)

### 2. Backend Service
**Create:** `backend/app/services/causal_factor_service.rb`
- Constructor: `initialize(country)`
- Main method: `call` returns `{ factors: [...], summary: {...} }`
- Each factor object includes:
  ```ruby
  {
    id: string,
    name: string,
    description: string,
    type: string,
    current_proxy_value: float,
    proxy_status: "rising" | "falling" | "stable",
    pct_change_3m: float,
    correlation_with_sector: float (rolling 12m Pearson corr),
    affected_sectors: [string],
    confidence: float (0-1),
    rank: integer
  }
  ```
- Private methods:
  - `load_config()` — YAML load pattern
  - `compute_correlation(proxy_indicator, sector_indicators, months_window = 12)` — Pearson correlation
  - `detect_proxy_status(proxy_series_data)` — trend detection
  - `rank_factors()` — sort by correlation strength + recent activity

### 3. Backend Controller
**Modify:** `backend/app/controllers/api/v1/countries_controller.rb`
- Add method:
  ```ruby
  def causal_factors
    country = Country.find(params[:id])
    data = Rails.cache.fetch("country_causal_factors/#{country.id}", expires_in: 1.hour) do
      CausalFactorService.new(country).call
    end
    render json: data
  end
  ```

### 4. Routes
**Modify:** `backend/config/routes.rb`
- Add to member block under countries resource: `get :causal_factors`

### 5. Frontend API Client
**Modify:** `frontend/api_client.py`
- Add function:
  ```python
  def get_country_causal_factors(country_id):
      return _get(f"/countries/{country_id}/causal_factors")
  ```

### 6. Frontend Components
**Modify:** `frontend/components.py`
- Add helper function `_build_factors_compact(factors_data)`:
  - Returns compact factor chips with name + status + correlation
  - Max 5 factors displayed
  - Each chip shows: factor name, correlation score (0.XX), affected sectors as tags
  - Color-coded by confidence/correlation strength (green=strong, yellow=moderate, red=weak)
  - Tooltip on hover shows description + current proxy value
- Modify `build_intelligence_panel()` signature to accept optional `factors_data` parameter
- Add factors section to right column (after narrative bullets, before closing)

### 7. Frontend Callbacks
**Modify:** `frontend/callbacks.py`
- Extend `update_intelligence_panel()` callback (lines 153-173):
  - Fetch `api_client.get_country_causal_factors(country_id)` in addition to cycle/summary
  - Pass factors_data to `build_intelligence_panel(cycle_data, summary_data, factors_data)`
  - Handle error gracefully (empty list if factors call fails)

### 8. Frontend Styling
**Modify:** `frontend/assets/style.css`
- Add CSS classes for factors:
  ```css
  .factors-label { ... }  /* Intel label styling for "Causal Factors" header */
  .factors-chips { ... }  /* Flex grid container */
  .factor-chip { ... }    /* Individual factor element with background color based on confidence */
  .factor-name { ... }    /* Factor name text */
  .factor-correlation { ... } /* Correlation score badge */
  .factor-sectors { ... } /* Affected sectors tags */
  ```

## Implementation Order
1. Create `causal_factors.yml` config file with factor definitions
2. Create `CausalFactorService` (no UI dependencies, test with Rails console)
3. Add controller action + route
4. Add frontend API client function
5. Add component helper functions for rendering
6. Extend callback to fetch and pass data
7. Update component styles
8. Test end-to-end

## Verification
1. **Backend:**
   - `curl http://localhost:8051/api/v1/countries/1/causal_factors` returns factors with data
   - Service correctly computes correlations (validate with 1-2 factors manually)
   - All 5 countries have factors defined in config

2. **Frontend:**
   - Country dropdown → factors appear in intelligence panel
   - Clicking country changes factors displayed
   - Hovering over factor chip shows description tooltip
   - Factor correlation scores displayed (0.XX format)
   - Affected sectors shown as small tags

3. **Edge cases:**
   - Empty factors list handled gracefully
   - Missing proxy series doesn't crash (returns empty or warning)
   - Insufficient data returns empty factors rather than error

## Notes
- No database migrations needed (config-driven)
- Reuses existing Indicator/DataPoint models for proxy series lookups
- Rolling 12-month correlation window matches business cycle window (consistency)
- Factors rankable by correlation strength + recent proxy volatility
- Future enhancement: LLM narrative generation for why factors matter
