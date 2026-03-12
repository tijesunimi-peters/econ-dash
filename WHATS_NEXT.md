# What's Next: Econ Dashboard Roadmap

**Current Status**: Phase 3 ✅ Complete (Real API Integration)
**Date**: 2026-03-12
**Next Priority**: Phase 4 — Supply Chain & Trade Flows

---

## Quick Decision Matrix

| Priority | Feature | Effort | Impact | Timeline | Owner |
|----------|---------|--------|--------|----------|-------|
| 🔴 **HIGH** | Phase 4: Trade Flows | 2-3 weeks | Very High | This week | TBD |
| 🟠 **MEDIUM** | More WB Indicators | 1-2 hours | Medium | Any time | Quick win |
| 🟠 **MEDIUM** | Confidence Intervals UI | 1-2 hours | Medium | Any time | Frontend |
| 🟡 **LOW** | ARIMA Forecasting | 3-4 hours | High | Next month | Analytics |
| 🟡 **LOW** | ML Anomaly Detection | 20+ hours | Very High | Q2 2026 | Advanced |

---

## 🎯 Recommended Next Steps (In Order)

### **Tier 1: Immediate (This Week)**

#### 1. **Production Deployment**
**Time**: 30 min
**Effort**: Trivial
**Impact**: Critical

```bash
# Deploy Phase 3 to production
docker-compose exec backend bin/rails db:migrate
docker-compose exec backend bin/rails structural_data:ingest
bin/solid_queue start  # Start nightly jobs

# Verify
curl http://api:8051/api/v1/countries/1/structural_forecast
```

**Checklist**:
- [ ] Run migrations
- [ ] Load initial data
- [ ] Start Solid Queue worker
- [ ] Monitor first ingest at 2:00 AM UTC
- [ ] Verify DataIngestLog entries

---

#### 2. **Phase 4: Trade Flows & Supply Chain** (NEXT BIG FEATURE)
**Time**: 2-3 weeks
**Effort**: High
**Impact**: Very High
**Status**: NOT STARTED

This completes the "Strategic Context" layer by adding trade dependencies.

**What it does**:
- Track country exports/imports by sector
- Show supply chain dependencies
- Identify trade bottleneck risks
- Map tariff impacts

**Data sources**:
- UN Comtrade API (free, comprehensive)
- World Bank trade data
- IMF Direction of Trade Statistics

**Architecture** (follows Phase 1-3 pattern):
```
Backend:
- TradeFlowClient service (UN Comtrade)
- TradeFlow, TradeBottleneck models
- trade_flows API endpoint

Frontend:
- Trade dependency visualization
- Supply chain risk heatmap
- Country pair flow diagrams

Jobs:
- IngestTradeDataJob (monthly, not nightly)
```

**Estimated LOC**: 800-1000 lines
**Estimated Cost**: 60-80 developer hours

---

### **Tier 2: High-Value Quick Wins (This Week - Next Week)**

#### 3. **Add More World Bank Indicators**
**Time**: 1-2 hours
**Effort**: Minimal
**Impact**: Medium

Just add more indicators to `WorldBankClient::INDICATORS`:
- Foreign direct investment flows
- Merchandise trade volumes
- Infrastructure investment
- Technology adoption rates

```ruby
# In world_bank_client.rb, add to INDICATORS:
fdi_inflows: "BX.KLT.DINV.CD",           # FDI inflows (USD)
merchandise_trade_pct: "NE.TRD.GNFS.CD", # Trade % of GDP
tech_exports: "TX.VAL.TECH.CD",          # High-tech exports
```

**Benefit**: Richer structural health metrics
**No API changes needed** — just runs on nightly ingest

---

#### 4. **Visualize Confidence Intervals on Sparklines**
**Time**: 1-2 hours
**Effort**: Minimal
**Impact**: Medium

Enhance sparkline visualization with confidence bands:

```python
# In components.py _build_mini_sparkline():
# Add shaded band around forecast line
# Color: rgba(orange, 0.2) for upper/lower bounds
```

**Benefit**: Better forecast visualization
**Frontend only** — no backend changes

---

### **Tier 3: Medium-Term Features (Next 1-2 Months)**

#### 5. **Cross-Country Percentile Rankings**
**Time**: 3-4 hours
**Effort**: Medium
**Impact**: High

Show how each country compares to others:
```
US GDP per Capita: $84,534 (🥇 1st out of 5)
US Population: 340M (🥇 1st out of 5)
US Unemployment: 4.2% (🥈 2nd — better than JP, DE)
```

**Implementation**:
- PercentileService calculates rank per metric
- API adds `percentile_rank`, `percentile_countries`
- Frontend shows rank badge

---

#### 6. **ARIMA/Prophet Forecasting**
**Time**: 3-4 hours
**Effort**: Medium
**Impact**: High

Replace linear regression with more sophisticated methods:

```python
# New forecast methods:
- ARIMA (handles trends + seasonality)
- Prophet (Facebook's forecasting library)
- LSTM neural networks (advanced)

# Add to TrendForecastService
```

**Benefit**: Better forecasts for non-linear trends
**Requires**: numpy, statsmodels, or Prophet library

---

#### 7. **Custom Alert Rules**
**Time**: 2-3 hours
**Effort**: Medium
**Impact**: Medium

Move alert thresholds from code to database:

```ruby
class AlertRule < ApplicationRecord
  # user_id, country_id, metric_type
  # condition: "value > 100" or "trend_change > 5%"
  # notification_type: email, in_app, webhook
end
```

**Benefit**: Users can customize alerts without code changes

---

### **Tier 4: Advanced Features (Q2 2026+)**

#### 8. **Machine Learning**

**A. Anomaly Detection** (20 hours)
- Isolation Forest for outliers
- Auto-flag unusual values
- Pattern detection

**B. Clustering** (15 hours)
- Group similar countries/regions
- Find peer economies
- Comparative analysis

**C. Causal Inference** (30 hours)
- Quantify policy impact
- A/B testing framework
- Counterfactual analysis

---

#### 9. **Real-Time Data Feeds** (10 hours)
- Weekly updates instead of daily
- High-frequency indicators
- Streaming architecture

---

#### 10. **Advanced Analytics Dashboard** (15 hours)
- Scenario analysis (what-if modeling)
- Correlation matrix visualization
- Custom metric builder
- Saved dashboards/views

---

## 📊 Full Roadmap Timeline

```
NOW         Q1 2026         Q2 2026         Q3 2026
│           │               │               │
Phase 3 ✅  Phase 4 →→→  Advanced Analytics  ML & Real-time
            Trade Flows     & Forecasting     Deep Dive

■ Complete  ■ In Progress   ■ Planned        ■ Future
```

---

## 🚀 How to Proceed

### **Option A: Aggressive Path (Recommended)**
1. **This week**: Deploy Phase 3, start Phase 4 research
2. **Week 2-3**: Implement Phase 4 (Trade Flows)
3. **Week 4**: Quick wins (confidence intervals, more indicators)
4. **May**: Percentile rankings + ARIMA forecasting
5. **June**: Custom alerts + ML features

**Timeline**: 3 months to Phase 4 + all quick wins

---

### **Option B: Measured Path**
1. **This week**: Deploy Phase 3
2. **Week 2**: Quick wins only (confidence intervals, indicators)
3. **Week 3-4**: User feedback collection
4. **May**: Phase 4 (Trade Flows)
5. **June+**: ML & advanced features

**Timeline**: 4 months to Phase 4, more user-focused

---

### **Option C: MVP Focus**
1. **This week**: Deploy Phase 3
2. **Week 2+**: User feedback on Phase 3 features
3. **Focus**: Perfecting existing features over new ones
4. **Defer**: Phase 4 until Phase 3 fully adopted

**Timeline**: Stability over features

---

## 📋 Decision Questions

**Q1: How important is trade flow data?**
- Very (Global supply chains are key context) → Do Phase 4 now
- Moderate (Nice to have) → Do after quick wins
- Low (Focus on other areas) → Skip for now

**Q2: Is forecasting accuracy critical?**
- Yes → Add ARIMA forecasting (Q2)
- Moderate → Current linear regression sufficient
- No → Skip for now

**Q3: Do users need percentile rankings?**
- Yes → High priority (medium effort)
- Maybe → Do after Phase 4
- No → Skip

**Q4: Are machine learning features in scope?**
- Yes → Plan for Q2/Q3
- Maybe → Depends on user feedback
- No → Stick to statistical/deterministic features

---

## ✅ Pre-Phase 4 Checklist

Before starting Phase 4, verify:

- [ ] Phase 3 deployed to production
- [ ] Solid Queue jobs running successfully
- [ ] Data ingest logs show consistent success
- [ ] API performance verified (<500ms)
- [ ] Documentation reviewed
- [ ] No critical bugs reported
- [ ] Database backups configured

---

## 🎓 Learning Resources

For whoever owns Phase 4:

**UN Comtrade API**
- Docs: https://comtradeplus.un.org/
- Coverage: 200+ countries, 5000+ products
- Free tier: 100 requests/hour

**Supply Chain Analysis**
- Eigenvector Centrality for bottlenecks
- Network analysis for dependencies
- Graph database considerations

**Trade Policy**
- Tariff data: World Bank WITS
- Regional trade: WTO statistics
- FTA tracking: USTR database

---

## 💡 Final Recommendation

**DO THIS NOW:**

1. ✅ **Deploy Phase 3** (30 min) — Get nightly jobs running
2. ✅ **Quick wins** (2-3 hours) — Low-hanging fruit (indicators, UI)
3. ✅ **Get user feedback** (1 week) — What do they want?
4. 🎯 **Phase 4 design** (1 week) — Plan trade flows feature

**Then decide**: Based on feedback, either:
- **Sprint Phase 4** (aggressive)
- **Build quick wins first** (measured)
- **Polish Phase 3** (conservative)

---

## 📞 Questions to Answer

Before picking the next big project:

1. **Who are your users?** (Analysts, traders, researchers?)
2. **What's their pain point?** (Missing trade data? Forecasts not accurate enough?)
3. **What's the success metric?** (Feature adoption? Performance improvement?)
4. **What's the timeline?** (This month? This quarter?)
5. **What's the team size?** (1 dev? 3 devs?)

**Answer these → Clear path forward** 🚀

