# Phase 3 Enhancement: Real API Integration

## Overview

Phase 3 now includes **automated data ingestion from World Bank API**, enabling production-ready structural metrics with:
- **6-year historical trends** (2019-2024) instead of single snapshot values
- **Sparkline visualizations** showing trend patterns in dashboard
- **Automatic data refreshes** via Rake task
- **Metadata tracking** (last updated, data source, trend direction)

## What Changed

### Backend

1. **New Service: WorldBankClient**
   - File: `backend/app/services/world_bank_client.rb`
   - Fetches demographic/economic indicators from World Bank API
   - Supports: Population, Life Expectancy, R&D %, Education Spending
   - Auto-retries on server errors, rate-limited (0.5s between calls)
   - No API key required (free tier)

2. **New Database Table: StructuralDataPoint**
   - Stores historical data points per metric
   - Composite unique constraint on (metric_id, date)
   - Indexes for efficient time-series queries
   - Supports 6+ years of annual data per metric

3. **Enhanced StructuralMetric Model**
   - New `has_many :data_points` relationship
   - New `trend_5year` method: Returns "up"/"down"/"stable" based on 5-year change
   - New `historical_data(years: 5)` method: Returns array of {date, value} for sparklines

4. **New Rake Task: structural_data:ingest**
   - Fetches data from World Bank API for all configured countries/indicators
   - Saves to database in transactional batches
   - Command: `docker-compose exec backend bin/rails structural_data:ingest`
   - Ingests ~90 data points in ~30 seconds

### Frontend

1. **Enhanced build_structural_health() Component**
   - New `_build_mini_sparkline()` helper creates inline trend charts
   - Displays 30px sparkline in each metric card
   - Shows trend indicator (↑/↓/→) from 5-year analysis
   - Displays "Updated: YYYY-MM-DD" and "Data source" metadata

2. **Updated CSS**
   - `.structural-sparkline` — Inline chart styling
   - `.structural-trend-indicator` — Arrow styling
   - `.structural-meta` — Footer metadata styling

### API Changes

**GET /countries/:id/structural_trends** now includes:
```json
{
  "metric_type": "population",
  "metric_label": "Population",
  "value": "340110988.0",
  "date": "2024-01-01",
  "data_source": "World Bank",
  "trend_5year": "up",
  "historical": [
    {"date": "2019-01-01", "value": 330226227},
    {"date": "2020-01-01", "value": 331577720},
    ...
  ]
}
```

New fields:
- `data_source` — "World Bank" or "Seed Data"
- `last_updated` — Last ingest timestamp
- `trend_5year` — Direction indicator
- `historical` — Array of 6 {date, value} tuples

## Data Ingestion

### Initial Setup

Run the ingestion task to populate database:

```bash
docker-compose exec backend bin/rails structural_data:ingest
```

Output: ~20 successful metric ingestions, ~91 total data points

### Available Metrics

**From World Bank API:**
- Population (SP.POP.TOTL)
- Life Expectancy (SP.DYN.LE00.IN)
- R&D as % GDP (GB.XPD.RSDV.GD.ZS)
- Education Spending % GDP (SE.XPD.TOTL.GD.ZS)

**From Seed Data (unchanged):**
- Median Age
- Labor Participation
- TFP Growth

### Data Coverage

- **Countries**: US, CA, JP, AU, DE
- **Timespan**: 2019-2024 (annual)
- **Update Frequency**: Manual on-demand (via Rake task)

## Visualization

Dashboard now shows:
1. **Sparkline chart** in each metric card — visual trend direction
2. **Trend arrow** (↑/↓/→) — 5-year direction indicator
3. **Update timestamp** — last ingest date
4. **Data source badge** — "World Bank" or "Seed Data"

Example: US Population card shows:
- Value: 340,110,988
- Trend: ↑ (up)
- Updated: 2024-01-01
- Source: World Bank
- Sparkline: Upward curve from 2019-2024

## Technical Details

### Data Model

**Before (Seed Data Only):**
```
StructuralMetric (1 row per metric type)
  - id, country_id, metric_type, value, date, unit, source
```

**After (With Historical):**
```
StructuralMetric (1 row per metric type)
  - id, country_id, metric_type, value, date, unit, source

StructuralDataPoint (Multiple rows per metric)
  - id, structural_metric_id, date, value
```

### Database Migrations

1. **create_structural_data_points.rb** — New table for time-series data
2. **fix_structural_metric_precision.rb** — Increased column precision for large values

### Error Handling

- **50x Server Errors** — Auto-retry up to 3 times with exponential backoff
- **40x Client Errors** — Log and skip, continue with next metric
- **Missing Data** — Gracefully handle null/empty values from API
- **Transactions** — Batch operations per country for atomicity

## Future Enhancements

1. **Automatic Scheduling** — Use Solid Queue to run ingest nightly
2. **Additional Indicators** — Add more World Bank metrics (unemployment, FDI, etc.)
3. **Debt Metrics API** — Integrate IMF for government/corporate debt data
4. **Forecast Layer** — Add trend projections (polynomial fit or ARIMA)
5. **Data Caching** — Cache World Bank responses for 24h to reduce API calls

## Testing

### Manual Testing

```bash
# Test World Bank API client
docker-compose exec backend bin/rails runner \
  'client = WorldBankClient.new; data = client.fetch_indicator("SP.POP.TOTL", "US"); puts data.length'

# Test trend calculation
docker-compose exec backend bin/rails runner \
  'metric = StructuralMetric.find_by(metric_type: "population"); puts metric.trend_5year'

# Test API endpoint
curl http://localhost:8051/api/v1/countries/1/structural_trends | jq '.structural_metrics[0]'

# Test historical data
curl http://localhost:8051/api/v1/countries/1/structural_trends | jq '.structural_metrics[0].historical'
```

### Database Verification

```bash
# Check ingested data points
docker-compose exec backend bin/rails runner \
  'puts "StructuralDataPoint count: #{StructuralDataPoint.count}"'

# View sample metric with history
docker-compose exec backend bin/rails runner \
  'metric = StructuralMetric.find_by(metric_type: "population"); puts metric.data_points.pluck(:date, :value)'
```

## Performance Notes

- **Ingest time**: ~30 seconds for 5 countries × 6 indicators
- **API rate limit**: 0.5s sleep between requests
- **Database size impact**: +91 rows for baseline ingest
- **Query performance**: Indexed lookups, group_by done in-memory

## Files Modified

### Backend
- `app/services/world_bank_client.rb` — NEW
- `app/models/structural_data_point.rb` — NEW
- `app/models/structural_metric.rb` — ENHANCED
- `app/controllers/api/v1/countries_controller.rb` — ENHANCED
- `lib/tasks/structural_data.rake` — NEW
- `db/migrate/20260312064423_create_structural_data_points.rb` — NEW
- `db/migrate/20260312070424_fix_structural_metric_precision.rb` — NEW

### Frontend
- `components.py` — ENHANCED
- `assets/style.css` — ENHANCED

## Rollback Strategy

If issues occur with World Bank data:

1. **Keep all rows**: Data exists in both seed (old) and WB (new) tables
2. **Revert to seed**: API controller falls back to `source == "seed_data"` filter
3. **Clear WB data**: `StructuralDataPoint.delete_all` + reset metric dates to today

## Notes

- **World Bank API** is free and doesn't require authentication
- **No breaking changes** — Existing seed data remains intact
- **Backwards compatible** — API returns both old and new data together
- **Optional feature** — Dashboard works fine with or without World Bank data
