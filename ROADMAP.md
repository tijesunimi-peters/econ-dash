# Econ Dashboard Roadmap

**Last Updated:** 2026-03-12
**Current Status:** Phase 4 ✅ COMPLETE (Trade Flows & Supply Chain)
**Next Priority:** Quick Wins & Tier 3 Features

---

## 📊 What's Complete

| Phase | Feature | Status | Notes |
|-------|---------|--------|-------|
| 1 | Policy Timeline | ✅ | 12 central bank/govt decisions × 5 countries |
| 2 | Market Sentiment | ✅ | 10 sentiment indicators (PMI, VIX, CCI, etc.) |
| 3 | Structural Health | ✅ | 13 metrics (demographics, debt, productivity) |
| 4 | Trade Flows | ✅ | Exports, imports, FDI, supply chain metrics |

---

## 🎯 What's Next (By Priority)

### Tier 2: Quick Wins (1-2 hours each)

#### 3️⃣ **More World Bank Indicators**
- **Time:** 1-2 hours
- **Effort:** Minimal
- **Impact:** Medium
- **What:** Add more indicators to `WorldBankClient::INDICATORS`
  - Foreign direct investment flows
  - Merchandise trade volumes
  - Infrastructure investment
  - Technology adoption rates
- **Benefit:** Richer structural health metrics without API changes
- **Example:** Add 3-4 more WB indicators for each metric type

---

#### 4️⃣ **Confidence Intervals on Sparklines**
- **Time:** 1-2 hours
- **Effort:** Minimal (frontend only)
- **Impact:** Medium
- **What:** Visualize forecast confidence bands
  - Shaded area around forecast line
  - Upper/lower bound visualization
  - Color: rgba(orange, 0.2) for bands
- **Where:** `frontend/components.py` → `_build_mini_sparkline()`
- **Benefit:** Better forecast visualization and uncertainty communication

---

### Tier 3: Medium-Term (1-2 months out)

#### 5️⃣ **Cross-Country Percentile Rankings**
- **Time:** 3-4 hours
- **Effort:** Medium
- **Impact:** High
- **What:** Show country rank vs peers
  - E.g., "🥇 1st in GDP per capita"
  - E.g., "🥈 2nd in unemployment"
- **Implementation:**
  - PercentileService calculates rank per metric
  - API adds `percentile_rank`, `percentile_countries` fields
  - Frontend shows rank badge on each metric
- **Benefit:** Instant country comparison context

---

#### 6️⃣ **ARIMA/Prophet Forecasting**
- **Time:** 3-4 hours
- **Effort:** Medium (backend-heavy)
- **Impact:** High
- **What:** Replace linear regression with time-series methods
  - ARIMA (handles trends + seasonality)
  - Prophet (Facebook's library, auto seasonality)
  - LSTM neural networks (advanced option)
- **Where:** Enhanced `TrendForecastService`
- **Benefit:** Better forecasts for non-linear trends
- **Requirements:** numpy, statsmodels, or Prophet library

---

#### 7️⃣ **Custom Alert Rules**
- **Time:** 2-3 hours
- **Effort:** Medium
- **Impact:** Medium
- **What:** Move alert thresholds from code to database
  ```ruby
  class AlertRule < ApplicationRecord
    # user_id, country_id, metric_type
    # condition: "value > 100" or "trend_change > 5%"
    # notification_type: email, in_app, webhook
  end
  ```
- **Benefit:** Users customize alerts without code changes

---

### Tier 4: Advanced Features (Q2 2026+)

#### 8️⃣ **Machine Learning**

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

#### 9️⃣ **Real-Time Data Feeds** (10 hours)
- Weekly updates instead of daily
- High-frequency indicators
- Streaming architecture

---

#### 🔟 **Advanced Analytics Dashboard** (15 hours)
- Scenario analysis (what-if modeling)
- Correlation matrix visualization
- Custom metric builder
- Saved dashboards/views

---

## 📅 Recommended Timeline

### Option A: Aggressive (Recommended)
1. **This week:** Review user feedback on Phase 4
2. **Week 2:** Quick wins (confidence intervals, more WB indicators)
3. **Week 3-4:** Percentile rankings + ARIMA forecasting
4. **May:** Custom alerts + advanced features
5. **June+:** ML features

**Timeline:** 2 months to all quick wins + Tier 3

---

### Option B: Measured
1. **This week:** Deploy Phase 4 to production
2. **Week 2:** Quick wins (confidence intervals only)
3. **Week 3-4:** User feedback collection
4. **May:** More indicators + percentiles
5. **June:** ARIMA + custom alerts

**Timeline:** 3 months to Tier 3, more user-focused

---

### Option C: MVP Focus
1. **This week:** Stabilize Phase 4
2. **Week 2+:** Monitor production, gather feedback
3. **Focus:** Perfect existing features over new ones
4. **Later:** Tier 2/3 based on user demand

**Timeline:** Stability over speed

---

## 🗺️ Implementation Roadmap Timeline

```
Now (Mar 2026)     Q2 2026              Q3 2026         Q4 2026
│                  │                    │               │
Phase 4 ✅       Quick Wins           Advanced        ML & Real-time
Complete         + Tier 3             Analytics       Deep Dive
                 (May-Jun)            (Jul-Aug)       (Sep+)
```

---

## 📋 Decision Framework

### Q1: What's the user priority?
- **Trade flows critical?** → Already complete ✅
- **Forecasting accuracy essential?** → Do ARIMA (Tier 3 #6)
- **Comparative analysis needed?** → Do percentiles (Tier 3 #5)
- **Real-time updates required?** → Plan Tier 4 #9

### Q2: What's the team bandwidth?
- **1 dev, 1-2 hours/week?** → Focus on quick wins (Tier 2)
- **1 dev full-time?** → Full Tier 3 in 1 month
- **2+ devs?** → Can parallelize Tier 2 + Tier 3

### Q3: What's the deployment timeline?
- **Production ready now?** → Deploy Phase 4
- **Still in beta?** → Stability phase (Option C)
- **User feedback needed?** → Measured path (Option B)

---

## ✅ Pre-Implementation Checklist

### Phase 4 Production Verification
- [ ] Trade flows API responding correctly
- [ ] All 35 seed records created (7 metrics × 5 countries)
- [ ] Alert thresholds working (supply chain concentration)
- [ ] Frontend renders without console errors
- [ ] Data sources labeled correctly (FRED vs World Bank vs Seed Data)
- [ ] Database performance acceptable
- [ ] Cache invalidation working

### Before Next Phase
- [ ] Phase 4 deployed to production
- [ ] Data ingest logs showing no errors
- [ ] API performance verified (<500ms)
- [ ] No critical bugs reported
- [ ] Documentation updated
- [ ] Database backups configured

---

## 📖 Architecture Notes for Future Work

### Tier 2 Implementation Patterns
- **More WB Indicators:** Add to `WorldBankClient::INDICATORS` hash, no schema changes
- **Confidence Intervals:** Extend `TrendForecastService.forecast_*` output with bounds

### Tier 3 Implementation Patterns
- **Percentiles:** Create `PercentileRankingService`, add calculated fields to metrics
- **ARIMA:** Extend `TrendForecastService` with statsmodels integration (Python gem wrapper)
- **Custom Rules:** New `AlertRule` model + logic in `BusinessCycleService`

### Tier 4 Implementation Patterns
- **ML Features:** Separate `app/services/ml/` namespace with scikit-learn/isolation_forest
- **Real-time:** WebSocket upgrade for frontend + event streaming on backend
- **Analytics:** New Dash tabs/pages, existing API enrichment

---

## 🎓 External Resources

### Time-Series Forecasting
- **ARIMA:** https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average
- **Prophet:** https://facebook.github.io/prophet/
- **StatsModels:** https://www.statsmodels.org/

### Machine Learning
- **Isolation Forest:** https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
- **Clustering:** https://scikit-learn.org/stable/modules/clustering.html

### Data Quality
- **World Bank API:** https://data.worldbank.org/developers/
- **FRED API:** https://fred.stlouisfed.org/docs/api/

---

## 💡 Final Recommendation

**NOW (This Week):**
1. ✅ Phase 4 complete & verified
2. Deploy to production
3. Gather user feedback

**NEXT (Week 2-3):**
1. Implement Quick Wins (Tier 2) in parallel
2. Plan Tier 3 based on feedback
3. Start design for ARIMA/percentiles

**THEN (Month 2):**
1. Release Tier 3 features
2. Stabilize production
3. Begin Tier 4 planning

This balanced approach ships value early (quick wins), responds to user feedback (gathered after Phase 4), and builds toward advanced features (planned but not rushed).

---

**Questions before proceeding?** Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) or [API_ENDPOINTS.md](API_ENDPOINTS.md) for technical details.
