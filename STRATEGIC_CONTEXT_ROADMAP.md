# Adding Strategic Context to Economic Dashboard

**Document Version**: 1.0
**Created**: 2026-03-12
**Status**: Planning
**Effort**: 8 weeks across 4 phases

---

## Overview

The current dashboard provides **tactical information** (what's happening now) but lacks **strategic context** (why it's happening and what comes next). This roadmap outlines a phased approach to add policy analysis, market expectations, structural trends, and trade flow data.

### Current Gap Analysis

**Tactical Data Available** ✅
- Sector YoY changes
- Business cycle phase positioning
- Anomalies & statistical outliers
- Momentum & acceleration metrics
- Causal factor correlations

**Strategic Context Missing** ❌
- Central bank policy decisions & timelines
- Market expectations & sentiment
- Long-term structural trends (demographics, debt)
- Supply chain & trade dependencies

---

## Architecture: Layered Information Model

```
┌─────────────────────────────────────────────────┐
│  STRATEGIC Context (WHY & WHAT'S NEXT)         │
├─────────────────────────────────────────────────┤
│ • Policy & Central Bank actions                │
│ • Market expectations & sentiment              │
│ • Long-term structural trends                  │
│ • Debt & financial stability                   │
│ • Supply chain & trade flows                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  TACTICAL Context (CURRENT STATE)              │
├─────────────────────────────────────────────────┤
│ • Sector YoY changes                           │
│ • Business cycle phase                         │
│ • Anomalies & outliers                         │
│ • Momentum & acceleration                      │
│ • Causal factors (correlation)                 │
└─────────────────────────────────────────────────┘
```

---

## Phase 1: Policy & Central Bank Context

**Timeline**: 2-4 weeks
**Effort**: Medium
**Impact**: High
**Status**: Not Started

### Goals
- Track central bank rate decisions
- Document government fiscal policy changes
- Show policy impact timeline and affected sectors
- Add policy context to dashboard

### Deliverables

#### 1.1 Database Model
```ruby
# backend/app/models/policy_decision.rb
class PolicyDecision < ApplicationRecord
  belongs_to :country

  # Columns:
  # - decision_type: interest_rate, qe, regulation, tariff
  # - announcement_date: when policy was announced
  # - effective_date: when policy takes effect
  # - description: text description of decision
  # - impact_sectors: JSON array of affected sectors
  # - expected_lag_months: delay before showing in economic data
  # - status: announced, effective, completed, reversed
end
```

**SQL Migration:**
```sql
CREATE TABLE policy_decisions (
  id SERIAL PRIMARY KEY,
  country_id INTEGER REFERENCES countries,
  decision_type VARCHAR(50),
  announcement_date DATE,
  effective_date DATE,
  description TEXT,
  impact_sectors JSONB,
  expected_lag_months INTEGER,
  status VARCHAR(20),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

#### 1.2 API Endpoint
```
GET /api/v1/countries/:id/policy_timeline
```

Returns:
```json
{
  "country_id": 1,
  "policies": [
    {
      "id": 1,
      "type": "interest_rate",
      "announcement": "2026-03-12",
      "effective": "2026-03-15",
      "description": "Fed raises rates 25bps to 5.50%",
      "impact_sectors": ["Financial", "Consumer", "Real Estate"],
      "lag_months": 1,
      "status": "effective"
    }
  ]
}
```

#### 1.3 Frontend Component
- `build_policy_timeline(policies)` function
- Timeline visualization showing policy decisions
- Color-coded by status (announced, effective, completed, reversed)
- Integration with intelligence panel

#### 1.4 Integration Point
- Add policy panel below intelligence panel in main dashboard
- Show last 20 policies chronologically
- Highlight policies that are currently effective

### Data Population

**Initial data for 5 countries** (manually curated):
- **US**: Last 10 Fed rate decisions, QE/QT cycles
- **Canada**: Last 10 BOC decisions, rate moves
- **Germany**: Last 10 ECB decisions
- **Japan**: Last 10 BOJ stimulus announcements
- **Australia**: Last 10 RBA rate decisions

**Example entries:**
```ruby
# US Federal Reserve Rate Hike
PolicyDecision.create!(
  country: Country.find_by(code: 'us'),
  decision_type: 'interest_rate',
  announcement_date: Date.parse('2026-03-12'),
  effective_date: Date.parse('2026-03-15'),
  description: 'Federal Reserve raises rates 25bps to 5.50%',
  impact_sectors: ['Financial', 'Consumer', 'Real Estate', 'Growth'],
  expected_lag_months: 1,
  status: 'effective'
)

# Germany Energy Policy
PolicyDecision.create!(
  country: Country.find_by(code: 'de'),
  decision_type: 'regulation',
  announcement_date: Date.parse('2025-06-01'),
  effective_date: Date.parse('2025-07-01'),
  description: 'New energy efficiency standards for manufacturing',
  impact_sectors: ['Manufacturing', 'Energy'],
  expected_lag_months: 2,
  status: 'effective'
)
```

### Success Criteria
- [ ] `policy_decisions` table created
- [ ] API endpoint returns data correctly
- [ ] Frontend component renders policy timeline
- [ ] 50+ policies populated across 5 countries
- [ ] Integration with dashboard complete
- [ ] No performance degradation

---

## Phase 2: Market Expectations & Sentiment

**Timeline**: 2-4 weeks
**Effort**: Medium
**Impact**: High
**Status**: Not Started

### Goals
- Track market sentiment indicators
- Show expectations (where market thinks rates/economy is going)
- Add forecast context alongside actual data
- Integrate with FRED API for some data

### Deliverables

#### 2.1 Database Model
```sql
CREATE TABLE market_sentiment (
  id SERIAL PRIMARY KEY,
  country_id INTEGER REFERENCES countries,
  metric_type VARCHAR(50),  -- cci, pmi, vix, yield_curve, etc
  value DECIMAL(10,2),
  date DATE,
  source VARCHAR(100),
  trend VARCHAR(20),  -- up, down, stable
  created_at TIMESTAMP
);
```

#### 2.2 Data Sources (Priority Order)

**Free/Low-Cost:**
1. FRED API - Inflation expectations, breakeven rates, yield curve
2. National statistics offices - PMI, consumer confidence
3. Yahoo Finance / Alpha Vantage - Stock market data, VIX
4. Central bank websites - Policy rate expectations

**Partially Paid:**
1. IHS Markit PMI (some free data)
2. Bond yield data (various sources)
3. FX expectations (derivative markets)

#### 2.3 Frontend Component
- `build_market_sentiment(sentiment_data)` function
- Display key sentiment indicators
- Show trend direction and comparison to historical average
- Color-code (green = positive, red = negative)

**Indicators to show:**
- Consumer Confidence Index (CCI)
- Manufacturing PMI (>50 = expansion, <50 = contraction)
- Fed Rate Expectations (vs current rate)
- Inflation Expectations (breakeven rate from FRED)
- VIX / Market Volatility Index
- Yield Curve Slope (10Y - 2Y yields)

#### 2.4 Integration Point
- New "Market Context" panel in dashboard
- Show alongside tactical data for comparison
- Highlight divergences (market expects different than current state)

### Data Population Strategy

**Week 1:** Manual data entry from central bank websites
- Current policy rates for each country
- Forward guidance (when do they hint at next move?)

**Week 2:** Integrate FRED API for US data
- Inflation expectations
- Yield curve data
- Fed funds futures

**Week 3:** Add PMI and sentiment indices manually
- Last 12 months of PMI data per country
- Latest CCI readings

**Week 4:** Build frontend components and integration

### Success Criteria
- [ ] `market_sentiment` table created
- [ ] FRED API integration working
- [ ] Historical data loaded (last 24 months)
- [ ] Frontend component renders sentiment panel
- [ ] Dashboard shows "Market Expects..." vs "Current State"
- [ ] No data stale by more than 1 week

---

## Phase 3: Structural & Long-Term Trends

**Timeline**: 4-6 weeks
**Effort**: High
**Impact**: Medium
**Status**: Not Started

### Goals
- Track demographics (population aging, labor participation)
- Show debt levels (government, corporate, household)
- Display productivity & innovation metrics
- Provide long-term sustainability context

### Deliverables

#### 3.1 Database Models
```sql
CREATE TABLE structural_metrics (
  id SERIAL PRIMARY KEY,
  country_id INTEGER REFERENCES countries,
  metric_type VARCHAR(50),  -- population, median_age, labor_participation, etc
  value DECIMAL(10,2),
  date DATE,
  unit VARCHAR(20),  -- %, years, billions, etc
  source VARCHAR(100),
  created_at TIMESTAMP
);

CREATE TABLE debt_metrics (
  id SERIAL PRIMARY KEY,
  country_id INTEGER REFERENCES countries,
  metric_type VARCHAR(50),  -- govt_debt_pct_gdp, corp_debt_ratio, hhd_debt_ratio
  value DECIMAL(10,2),
  date DATE,
  unit VARCHAR(20),
  source VARCHAR(100),
  created_at TIMESTAMP
);
```

#### 3.2 Data Sources

**World Bank API:**
- Population size
- Population growth rate
- Median age
- Labor force participation rate
- Life expectancy

**IMF Database:**
- Government debt as % of GDP
- Budget balance
- Current account balance

**National Statistics Offices:**
- Unemployment rate
- Dependency ratio (working-age pop / dependents)
- R&D spending as % GDP
- Patent filings

**OECD Database:**
- Labor productivity growth
- Total factor productivity
- Innovation indicators

#### 3.3 Frontend Component
- `build_structural_trends(structural_data)` function
- Display 3 sections: Demographics, Debt & Stability, Productivity
- Show multi-year trends (sparklines)
- Alert if metrics reach concerning levels

**Metrics to display:**

**Demographics:**
- Median age (aging → lower growth)
- Population growth rate (positive = expansion)
- Labor force participation (declining = pressure)
- Dependency ratio (aging = fiscal pressure)

**Debt & Stability:**
- Government debt % GDP (>90% = concerning)
- Corporate debt ratio (>3x EBITDA = risky)
- Household debt % income (>100% = stretched)
- Debt service coverage ratio

**Productivity & Innovation:**
- Labor productivity growth rate
- R&D as % GDP
- Patent filings per capita
- Education investment

#### 3.4 Integration Point
- New "Structural Health" panel in dashboard
- Shows long-term context ("Why this economy faces these headwinds")
- Helps explain why certain sectors are struggling

### Data Population Strategy

**Week 1:** API integration
- Connect to World Bank API
- Connect to IMF database
- Download historical data (last 10 years)

**Week 2:** Data cleaning & normalization
- Standardize units
- Handle missing data
- Create consistent date ranges

**Week 3:** Frontend components
- Build metrics displays
- Create sparklines for trends
- Add alert thresholds

**Week 4:** Integration & testing
- Add to dashboard layout
- Performance testing
- Data validation

### Success Criteria
- [ ] Historical structural data loaded (10+ years)
- [ ] All 5 countries have complete demographic data
- [ ] Debt metrics loaded from IMF
- [ ] Frontend component renders structural panel
- [ ] Dashboard shows aging population vs labor growth
- [ ] Debt sustainability metrics visible

---

## Phase 4: Supply Chain & Trade Flows

**Timeline**: 4-6 weeks
**Effort**: High
**Impact**: Medium
**Status**: Not Started

### Goals
- Show top trading partners per country
- Display trade concentration risks
- Track supply chain dependencies
- Identify vulnerability points

### Deliverables

#### 4.1 Database Model
```sql
CREATE TABLE trade_flows (
  id SERIAL PRIMARY KEY,
  country_from_id INTEGER REFERENCES countries,
  country_to_id INTEGER REFERENCES countries,
  product_category VARCHAR(100),  -- semiconductors, energy, agriculture, etc
  volume DECIMAL(15,2),  -- in billions USD
  percentage_of_exports DECIMAL(5,2),  -- % of total exports
  percentage_of_gdp DECIMAL(5,2),  -- % of exporting country's GDP
  date DATE,
  trend VARCHAR(20),  -- up, down, stable
  risk_level VARCHAR(20),  -- low, medium, high
  created_at TIMESTAMP
);
```

#### 4.2 Data Source
- **UN Comtrade Database** (free, comprehensive)
  - HS code product classification
  - Bilateral trade flows
  - Monthly updates available

**API Integration:**
```python
# Use python-comtrade or similar library
from comtrade import API

api = API()
df = api.get_data(
    r={'USA'},  # reporter
    p={'CHN'},  # partner
    freq='M',   # monthly
    ps='recent'  # recent years
)
```

#### 4.3 Frontend Component
- `build_trade_dependencies(trade_data)` function
- Show top 5 export destinations
- Show top 5 import sources
- Highlight concentration risk
- Flag if >30% exports to single partner

**Example display:**
```
Export Destinations:
  🇨🇳 China: 25.3% of exports ($120B) ⚠️ HIGH CONCENTRATION
  🇯🇵 Japan: 12.1% of exports ($57B)
  🇪🇺 EU: 18.5% of exports ($88B)
  🇲🇽 Mexico: 8.2% of exports ($39B)
  🇰🇷 South Korea: 6.4% of exports ($30B)

Import Sources:
  🇨🇳 China: 38.2% of imports ($180B) 🔴 CRITICAL CONCENTRATION
  🇩🇪 Germany: 12.1% of imports ($57B)
  ...
```

#### 4.4 Integration Point
- New "Trade Dependencies" panel in dashboard
- Identify vulnerability to geopolitical events
- Link to supply chain disruption risks
- Show if causal factors are trade-related

### Data Population Strategy

**Week 1:** UN Comtrade API integration
- Download bilateral trade data
- Last 10 years for each country pair
- Focus on top 20 trading partners per country

**Week 2:** Data processing
- Aggregate to country level
- Calculate concentration ratios
- Identify risk levels

**Week 3:** Frontend components
- Build trade partner lists
- Create concentration visualizations
- Add risk warnings

**Week 4:** Integration & analysis
- Link trade data to causal factors
- Show when geopolitical events affect trade
- Add to dashboard

### Success Criteria
- [ ] UN Comtrade data loaded for all country pairs
- [ ] Top export/import partners identified
- [ ] Trade concentration risk calculated
- [ ] Frontend component renders trade panel
- [ ] High-concentration trades flagged with warnings
- [ ] Historical trends shown (5+ years)

---

## Implementation Timeline

### Week 1-2: Phase 1 (Policy Timeline)
- [ ] Create `policy_decisions` table
- [ ] Build API endpoint
- [ ] Create frontend component
- [ ] Manually populate 50+ policies
- [ ] Integration test

### Week 3-4: Phase 2 (Market Sentiment)
- [ ] Create `market_sentiment` table
- [ ] Integrate FRED API
- [ ] Build sentiment component
- [ ] Load historical data (24 months)
- [ ] Integration test

### Week 5-6: Phase 3 (Structural Trends)
- [ ] Create structural metrics tables
- [ ] Integrate World Bank & IMF APIs
- [ ] Build structural trends component
- [ ] Load historical data (10 years)
- [ ] Integration test

### Week 7-8: Phase 4 (Trade Flows)
- [ ] Create `trade_flows` table
- [ ] Integrate UN Comtrade
- [ ] Build trade dependencies component
- [ ] Load historical data (10 years)
- [ ] Integration test

### Week 9+: Polish & Documentation
- [ ] Performance optimization
- [ ] Error handling & validation
- [ ] Documentation updates
- [ ] Dashboard layout refinement
- [ ] User testing & feedback

---

## Dashboard Layout: Strategic Context

### Before (Current)
```
┌─────────────────────────────────────────┐
│          Business Cycle Panel           │
├─────────────────────────────────────────┤
│ [Cycle Clock] [Leading Indicators]      │
│ [Recommendations] [Causal Factors]      │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│       Sector Momentum Rankings          │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│           Anomalies Alert               │
└─────────────────────────────────────────┘
```

### After (With Strategic Context)
```
┌──────────────────────────────────────────────────┐
│              STRATEGIC CONTEXT                  │
├──────────────┬───────────────┬──────────────────┤
│ Policy       │ Market        │ Structural       │
│ Timeline     │ Sentiment     │ Trends           │
│              │               │                  │
│ Last 5       │ CCI, PMI,     │ Debt %GDP,       │
│ decisions    │ Rate Exp,     │ Demographics,    │
│              │ VIX           │ Productivity     │
└──────────────┴───────────────┴──────────────────┘
         ↓ FILTERS & EXPLAINS
┌──────────────────────────────────────────────────┐
│              TACTICAL SNAPSHOT                   │
├──────────────────────────────────────────────────┤
│ Business Cycle | Sector Momentum | Anomalies    │
└──────────────────────────────────────────────────┘
         ↓ SHOWS CURRENT STATE
┌──────────────────────────────────────────────────┐
│         DETAILED ANALYSIS (Tabs)                │
├──────────────────────────────────────────────────┤
│ [Sectors] [Momentum] [Anomalies] [Trade] [Corr] │
│                                                  │
│ <Detailed analysis content>                     │
└──────────────────────────────────────────────────┘
```

### Information Flow
```
WHY does this matter?          WHAT is happening?       WHAT should I do?
(Strategic Context) ────→     (Tactical Data)    ────→  (Actions)

Policy Timeline                Sector Momentum           → Buy/Sell
Market Expectations      →     Cycle Phase         →     → Hedge
Debt/Demographics              Anomalies                 → Exit
Trade Partners                 Leading Indicators       → Hold
                                                        → Monitor
```

---

## Data Sources Summary

### Tier 1: Free, High-Quality (Start Here)
| Data | Source | API | Frequency |
|------|--------|-----|-----------|
| Interest Rates | Central Bank websites | Manual | Daily |
| Inflation Expectations | FRED (Federal Reserve) | ✅ Yes | Daily |
| Consumer Confidence | National stats offices | Manual | Monthly |
| PMI | National statistics | Manual | Monthly |
| Trade Data | UN Comtrade | ✅ Yes | Monthly |
| Demographics | World Bank | ✅ Yes | Annual |
| Debt Data | IMF | Manual | Annual |

### Tier 2: Partially Free
| Data | Source | Effort | Frequency |
|------|--------|--------|-----------|
| Stock Market | Yahoo Finance, Alpha Vantage | Low | Real-time |
| Bond Yields | FRED, Yahoo | Low | Daily |
| FX Rates | FRED, Yahoo | Low | Daily |

### Tier 3: Paid (Skip for MVP)
| Data | Source | Cost | Frequency |
|------|--------|------|-----------|
| Detailed Sentiment | Bloomberg | $$$$ | Real-time |
| Supply Chain Detail | Logistics firms | $$$ | Daily |
| Geopolitical Risk | Stratfor | $$$ | Daily |

---

## Priority Matrix: Start Here

### High Impact + Low Effort ✅ DO FIRST
- **Phase 1: Policy Timeline** (manual data entry + simple UI)
- **Phase 2: Market Sentiment (Basics)** (FRED API + manual data)
- **Phase 4: Trade Partners** (UN Comtrade API)

### High Impact + Medium Effort ✅ DO SECOND
- **Phase 2: Fed Rate Expectations**
- **Phase 3: Debt Metrics**
- **Phase 3: Demographics**

### Medium Impact + High Effort → DEFER
- Detailed supply chain mapping
- Geopolitical risk scoring
- Real-time sentiment analysis (requires paid APIs)

---

## Success Metrics

### Phase 1 Completion
- [ ] Policy decisions visible on dashboard
- [ ] User can see "why" the economy is moving (policy context)
- [ ] 50+ policies across 5 countries
- [ ] Performance: <100ms additional load time

### Phase 2 Completion
- [ ] Market sentiment panel shows current expectations
- [ ] Users can see divergences (market expects X, but cycle shows Y)
- [ ] Data refreshes daily with minimal manual effort
- [ ] All 5 countries have sentiment data

### Phase 3 Completion
- [ ] Structural trends visible (aging population, debt levels)
- [ ] Dashboard explains long-term constraints
- [ ] 10+ years of historical data per country
- [ ] Alerts for concerning debt/demographic levels

### Phase 4 Completion
- [ ] Trade dependencies visible
- [ ] Supply chain vulnerabilities flagged
- [ ] Trade concentration risks highlighted
- [ ] Link between causal factors and trade visible

### Overall Success
- Dashboard now answers: **"Why is the economy moving this way?"**
- Users understand both tactical (now) and strategic (future) context
- Information completeness improved from 6.5/10 to 9/10

---

## Notes & Assumptions

### Data Availability
- All 5 countries have open central banks (public data available)
- World Bank API will have historical demographics
- UN Comtrade has comprehensive trade statistics
- FRED API publicly available for US data

### Technical Assumptions
- Rails backend can handle additional API calls without bottleneck
- Postgres can handle 4 new tables with efficient indexing
- Dash frontend can render additional panels without lag
- No paid APIs required for MVP

### Scope Boundaries
- **NOT included:** Real-time geopolitical events, social media sentiment, earnings forecasts
- **NOT included:** Predictive modeling (only show data + context)
- **NOT included:** Automated policy analysis (manual curation)

### Maintenance Burden
- Policy decisions: Manual entry as they happen (~5/week per country)
- Market sentiment: Semi-automated (FRED API + manual PMI/CCI)
- Structural metrics: Annual updates from World Bank/IMF
- Trade flows: Monthly updates from UN Comtrade

---

## Related Documents

- `PROJECT.md` - Overall dashboard architecture
- `API_ENDPOINTS.md` - Current API endpoints (will add new ones)
- `DEVELOPER_GUIDE.md` - Dev workflow and setup
- `STATUS.md` - Current feature checklist

---

## Questions & Contact

For implementation questions or status updates on this roadmap, see:
- Backend architecture: Check `backend/` directory
- Frontend components: Check `frontend/components.py`
- Current dashboard: Running at `http://localhost:8050`

---

**Last Updated**: 2026-03-12
**Status**: Planning - Ready to begin Phase 1
**Next Steps**: Start with policy timeline data entry and backend model
