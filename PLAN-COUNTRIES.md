# Add Japan, Australia, and Germany to Economic Dashboard

## Context
The dashboard currently supports US and Canada. Adding Japan, Australia, and Germany. All use FRED OECD series — no new API clients needed. All series IDs below verified with HTTP 200 on fred.stlouisfed.org.

## Files to Modify

### 1. `backend/db/seeds.rb` — Append 3 country blocks
Follow the exact `find_or_create_by!` pattern as US/CA. All `source: "FRED"`.

**Japan (JP)** — 8 sectors, 13 indicators:
| Sector | Sub-Industry | Series ID | Name | Unit | Freq |
|--------|-------------|-----------|------|------|------|
| Manufacturing | Overall Manufacturing | JPNPROINDMISMEI | Industrial Production Index | Index | monthly |
| Labour | Employment | LRUNTTTTJPM156S | Unemployment Rate | Percent | monthly |
| Labour | Employment | LFEMTTTTJPM647S | Employment Level | Persons | monthly |
| Housing | Prices | QJPN368BIS | Residential Property Prices | Index 2010=100 | quarterly |
| Consumer | Spending | JPNSLRTTO02IXOBM | Retail Sales | Index | monthly |
| Consumer | Confidence | CSCICP03JPM665S | Consumer Confidence | Index | monthly |
| Financial | Interest Rates | IRSTCI01JPM156N | Call Rate | Percent | monthly |
| Financial | Interest Rates | IRLTLT01JPM156N | 10-Year Bond Yield | Percent | monthly |
| Inflation | Consumer Prices | JPNCPIALLMINMEI | CPI All Items | Index | monthly |
| Inflation | Consumer Prices | JPNCPICORMINMEI | Core CPI | Index | monthly |
| Trade | Trade Balance | XTEXVA01JPM667S | Exports | USD | monthly |
| Trade | Trade Balance | XTIMVA01JPM667S | Imports | USD | monthly |
| Energy | GDP | NAEXKP01JPQ189S | GDP (energy proxy) | Index | quarterly |

**Australia (AU)** — 8 sectors, 13 indicators:
| Sector | Sub-Industry | Series ID | Name | Unit | Freq |
|--------|-------------|-----------|------|------|------|
| Manufacturing | Overall Manufacturing | AUSPROINDQISMEI | Industrial Production Index | Index | quarterly |
| Labour | Employment | LRUNTTTTAUM156S | Unemployment Rate | Percent | monthly |
| Labour | Employment | LFEMTTTTAUM647S | Employment Level | Persons | monthly |
| Housing | Prices | QAUR628BIS | Residential Property Prices | Index 2010=100 | quarterly |
| Consumer | Spending | SLRTTO01AUQ659S | Retail Sales | Percent Change | quarterly |
| Consumer | Confidence | CSCICP03AUM665S | Consumer Confidence | Index | monthly |
| Financial | Interest Rates | IRSTCI01AUM156N | Cash Rate | Percent | monthly |
| Financial | Interest Rates | IRLTLT01AUM156N | 10-Year Bond Yield | Percent | monthly |
| Inflation | Consumer Prices | AUSCPIALLQINMEI | CPI All Items | Index | quarterly |
| Inflation | Consumer Prices | AUSCPICORQINMEI | Core CPI | Index | quarterly |
| Trade | Trade Balance | XTEXVA01AUM667S | Exports | USD | monthly |
| Trade | Trade Balance | XTIMVA01AUM667S | Imports | USD | monthly |
| Energy | GDP | NAEXKP01AUQ657S | GDP (energy proxy) | AUD | quarterly |

**Germany (DE)** — 8 sectors, 13 indicators:
| Sector | Sub-Industry | Series ID | Name | Unit | Freq |
|--------|-------------|-----------|------|------|------|
| Manufacturing | Overall Manufacturing | DEUPROINDMISMEI | Industrial Production Index | Index | monthly |
| Labour | Employment | LRHUTTTTDEM156S | Unemployment Rate | Percent | monthly |
| Labour | Employment | LFEMTTTTDEQ647S | Employment Level | Persons | quarterly |
| Housing | Prices | QDER628BIS | Residential Property Prices | Index 2010=100 | quarterly |
| Consumer | Spending | DEUSLRTTO02IXOBM | Retail Sales | Index | monthly |
| Consumer | Confidence | CSCICP03DEM665S | Consumer Confidence | Index | monthly |
| Financial | Interest Rates | IR3TIB01DEM156N | 3-Month Interbank Rate | Percent | monthly |
| Financial | Interest Rates | IRLTLT01DEM156N | 10-Year Bund Yield | Percent | monthly |
| Inflation | Consumer Prices | DEUCPIALLMINMEI | CPI All Items | Index | monthly |
| Inflation | Consumer Prices | DEUCPICORMINMEI | Core CPI | Index | monthly |
| Trade | Trade Balance | XTEXVA01DEM667S | Exports | USD | monthly |
| Trade | Trade Balance | XTIMVA01DEM667S | Imports | USD | monthly |
| Energy | GDP | NAEXKP01DEQ189S | GDP (energy proxy) | Index | quarterly |

### 2. `backend/config/indicator_classifications.yml` — Append 3 sections

```yaml
jp:
  leading:
    - CSCICP03JPM665S   # Consumer Confidence
    - QJPN368BIS        # House Prices
    - LRUNTTTTJPM156S   # Unemployment Rate (inverted)
  coincident:
    - JPNPROINDMISMEI   # Industrial Production
    - LFEMTTTTJPM647S   # Employment Level
    - JPNSLRTTO02IXOBM  # Retail Sales
  lagging:
    - LRUNTTTTJPM156S   # Unemployment Rate
    - JPNCPIALLMINMEI   # CPI
    - IRSTCI01JPM156N   # Call Rate
  inverted:
    - LRUNTTTTJPM156S
  sector_cycle_map:
    expansion: [Consumer, Financial, Energy]
    peak: [Energy, Inflation]
    contraction: [Financial, Trade]
    trough: [Housing, Manufacturing]

au:
  leading:
    - CSCICP03AUM665S   # Consumer Confidence
    - QAUR628BIS        # House Prices
    - LRUNTTTTAUM156S   # Unemployment Rate (inverted)
  coincident:
    - AUSPROINDQISMEI   # Industrial Production
    - LFEMTTTTAUM647S   # Employment Level
    - SLRTTO01AUQ659S   # Retail Sales
  lagging:
    - LRUNTTTTAUM156S   # Unemployment Rate
    - AUSCPIALLQINMEI   # CPI
    - IRSTCI01AUM156N   # Cash Rate
  inverted:
    - LRUNTTTTAUM156S
  sector_cycle_map:
    expansion: [Consumer, Financial, Energy]
    peak: [Energy, Inflation]
    contraction: [Financial, Trade]
    trough: [Housing, Manufacturing]

de:
  leading:
    - CSCICP03DEM665S   # Consumer Confidence
    - QDER628BIS        # House Prices
    - LRHUTTTTDEM156S   # Unemployment Rate (inverted)
  coincident:
    - DEUPROINDMISMEI   # Industrial Production
    - LFEMTTTTDEQ647S   # Employment Level
    - DEUSLRTTO02IXOBM  # Retail Sales
  lagging:
    - LRHUTTTTDEM156S   # Unemployment Rate
    - DEUCPIALLMINMEI   # CPI
    - IR3TIB01DEM156N   # Interbank Rate
  inverted:
    - LRHUTTTTDEM156S
  sector_cycle_map:
    expansion: [Consumer, Financial, Energy]
    peak: [Energy, Inflation]
    contraction: [Financial, Trade]
    trough: [Housing, Manufacturing]
```

### 3. Frontend — 3 files

**`frontend/app.py`** (line 11): Title → `"Economic Dashboard"`

**`frontend/layouts.py`**:
- Line 14: Subtitle → `"Global Economic Sector Trends and Drill-Down"`
- Line 62: Tab label → `"Compare"` (was `"US vs Canada"`)

**`frontend/callbacks.py`** (compare tab, ~line 260):
- Replace hardcoded "pick first other country" with a `dcc.Dropdown` listing all countries except the current one
- Default to first other country, render comparison chart below

### 4. Seed + ingest after code changes
```
docker compose exec backend rails db:seed
docker compose exec backend rails data:ingest
docker compose restart frontend
```

## Verification
1. `curl http://localhost:8051/api/v1/countries` — 5 countries
2. `curl http://localhost:8051/api/v1/countries/{3,4,5}/business_cycle` — all return phase data
3. Country dropdown shows all 5
4. Compare tab has country selector dropdown
