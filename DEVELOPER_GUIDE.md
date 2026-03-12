# Developer Guide — Economic Dashboard

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- 3 available ports: 6543 (DB), 8050 (Frontend), 8051 (Backend)

### Initial Setup
```bash
cd /home/admin/econ-dashboard
docker compose up -d
docker compose exec backend bin/rails db:create db:migrate db:seed
docker compose exec backend bin/rails data:ingest
```

### Access Dashboard
- **Frontend:** http://localhost:8050
- **Backend API:** http://localhost:8051/api/v1/
- **Database:** localhost:6543 (PostgreSQL)

---

## Architecture

### Backend (Rails 8.1 API)
Located in `backend/` directory.

**Key directories:**
```
app/
  controllers/api/v1/       # REST endpoint handlers
    countries_controller.rb       # Main endpoints for countries
    sectors_controller.rb         # Sector endpoints
    indicators_controller.rb      # Indicator time-series endpoints
  models/                   # ActiveRecord models
    country.rb
    sector.rb
    sub_industry.rb
    indicator.rb
    data_point.rb
  services/                 # Business logic services
    business_cycle_service.rb     # Leading index & phase detection
    causal_factor_service.rb      # Correlation analysis
    [other services]              # Percentiles, anomalies, momentum, etc.
  jobs/                     # Background jobs
    ingest_data_job.rb      # Scheduled data pulls from FRED

config/
  causal_factors.yml        # Factor definitions per country/sector
  indicator_classifications.yml  # Leading/lagging indicators per country
  routes.rb                 # REST routes
```

**Database schema:**
```
countries (id, name, code)
├── sectors (id, country_id, name, description)
│   └── sub_industries (id, sector_id, name, description)
│       └── indicators (id, sub_industry_id, name, source_series_id, frequency)
│           └── data_points (id, indicator_id, date, value)
```

### Frontend (Plotly Dash)
Located in `frontend/` directory.

**Key files:**
```
app.py                # Dash app initialization & main layout
layouts.py            # Component builders (tabs, cards, charts)
components.py         # Reusable component generators
  - build_country_dropdown()
  - build_sector_cards()
  - build_momentum_table()
  - build_cycle_clock()
  - build_factors_compact()
  - build_intelligence_panel()
callbacks.py          # Event handlers for user interactions
api_client.py         # HTTP wrapper for Rails API
assets/style.css      # Inline CSS styling
```

---

## Common Tasks

### Add a New Endpoint

1. **Define in `config/routes.rb`:**
```ruby
get :your_endpoint, on: :member  # For /countries/:id/your_endpoint
get :collection_endpoint          # For /countries/collection_endpoint
```

2. **Implement in `app/controllers/api/v1/countries_controller.rb`:**
```ruby
def your_endpoint
  country = Country.find(params[:id])
  data = Rails.cache.fetch("key_#{country.id}", expires_in: 1.hour) do
    YourService.new(country).call
  end
  render json: data
end
```

3. **Create service `app/services/your_service.rb`:**
```ruby
class YourService
  def initialize(country)
    @country = country
  end

  def call
    # Your business logic
    { result: "data" }
  end
end
```

4. **Test:**
```bash
curl http://localhost:8051/api/v1/countries/1/your_endpoint
```

### Add a New Country

1. **Get country data from FRED:**
   - Use OECD naming patterns: `CSCICP03<CC>M665S` (e.g., `CSCICP03FRM665S` for France)
   - Identify required series IDs for each sector

2. **Update `backend/db/seeds.rb`:**
```ruby
country = Country.find_or_create_by!(name: "France", code: "FR")
sector = country.sectors.find_or_create_by!(name: "Manufacturing")
sub = sector.sub_industries.find_or_create_by!(name: "Production")
Indicator.find_or_create_by!(
  sub_industry_id: sub.id,
  name: "Industrial Production",
  source_series_id: "FRPROINDMISMEI",
  frequency: "monthly"
)
```

3. **Update `backend/config/indicator_classifications.yml`:**
```yaml
fr:  # lowercase country code
  leading:
    - CSCICP03FRM665S    # Consumer Confidence
    - QFRA628BIS         # House Prices
  coincident:
    - FRPROINDMISMEI     # Industrial Production
  lagging:
    - LRUNTTTTFRM156S    # Unemployment
  inverted:
    - LRUNTTTTFRM156S
  sector_cycle_map:
    expansion: [Consumer, Financial]
    # ... other phases
```

4. **Update `backend/config/causal_factors.yml`:**
```yaml
fr:
  sectors:
    Energy:
      factors:
        - id: fr_oil_import
          name: "Oil Imports"
          description: "..."
          type: external_dependency
          proxy_series_id: DCOILWTICO
          sensitivity: high
          affected_sectors: ["Energy", "Manufacturing"]
```

5. **Seed and ingest:**
```bash
docker compose exec backend bin/rails db:seed
docker compose exec backend bin/rails data:ingest
docker compose restart frontend
```

6. **Verify:**
```bash
curl http://localhost:8051/api/v1/countries | jq '.[].code'
```

### Add a New Service Computation

Example: Adding a new indicator analysis (e.g., volatility, trend strength).

1. **Create service:**
```ruby
class VolatilityService
  def initialize(indicator)
    @indicator = indicator
  end

  def call
    points = @indicator.data_points.order(:date)
    values = points.map(&:value)
    { volatility: compute_volatility(values), trend: detect_trend(values) }
  end

  private

  def compute_volatility(values)
    mean = values.sum / values.size
    variance = values.sum { |v| (v - mean)**2 } / values.size
    Math.sqrt(variance)
  end

  def detect_trend(values)
    # Your trend detection logic
  end
end
```

2. **Expose via new endpoint:**
```ruby
def volatility
  indicator = Indicator.find(params[:id])
  data = VolatilityService.new(indicator).call
  render json: data
end
```

### Debug Database Issues

```bash
# Connect to PostgreSQL directly
docker exec econ-dashboard-db-1 psql -U econ -d econ_dashboard_development

# Common queries
SELECT COUNT(*) FROM countries;
SELECT COUNT(*) FROM data_points;
SELECT DISTINCT country_id FROM indicators;

# Clear data
TRUNCATE data_points;
DELETE FROM indicators;
DELETE FROM sub_industries;
DELETE FROM sectors;
DELETE FROM countries;
```

### Clear Cache

After code changes to services, clear Rails cache:
```bash
docker compose exec backend bin/rails runner 'Rails.cache.clear'
# OR
curl -X POST http://localhost:8051/rails/cache/clear
# OR restart backend
docker compose restart backend
```

### View Logs

```bash
# Backend
docker compose logs -f backend

# Frontend
docker compose logs -f frontend

# Database
docker compose logs -f db

# All services
docker compose logs -f
```

---

## Important Patterns & Conventions

### Service Objects
All complex business logic lives in services under `app/services/`. Services:
- Have single responsibility
- Are initialized with context (country, indicator, etc.)
- Have a `call` method that returns a hash
- Handle data fetching and transformations
- Are tested separately from controllers

### Caching
Use Rails cache for expensive operations:
```ruby
data = Rails.cache.fetch("unique_key/#{id}", expires_in: 1.hour) do
  ExpensiveService.new(object).call
end
```

### API Response Format
All endpoints return JSON hashes (not arrays at root level):
```json
{ "key": "value" }
```

### Error Handling
Return HTTP status codes and error messages:
```ruby
return render json: { error: "Invalid phase" }, status: :bad_request unless valid_phases.include?(phase)
```

### Rails Console
Use Docker to access Rails console:
```bash
docker compose exec backend bin/rails console
# Then
Country.all
Indicator.find(1).data_points.count
BusinessCycleService.new(Country.first).call
```

---

## Testing

### Manual API Testing
```bash
# List countries
curl http://localhost:8051/api/v1/countries

# Get country with sectors
curl http://localhost:8051/api/v1/countries/1

# Business cycle analysis
curl http://localhost:8051/api/v1/countries/1/business_cycle | jq '.current_phase'

# Causal factors
curl http://localhost:8051/api/v1/countries/1/causal_factors | jq '.factors[0]'

# Cycle phase filtering
curl 'http://localhost:8051/api/v1/countries/by_cycle_phase/expansion' | jq '.countries[].name'

# Compare countries
curl 'http://localhost:8051/api/v1/countries/1/compare/2' | jq keys
```

### Frontend Testing
Open http://localhost:8050 and:
1. Select different countries from dropdown
2. Verify sectors load and update
3. Click sectors to drill down to sub-industries
4. Click sub-industries to view time-series charts
5. Check Momentum tab for scoreboard
6. Check Compare tab for heatmap
7. Verify Intelligence Panel shows causal factors

---

## Performance Tips

1. **Database indexing:** Most queries are on `country_id`, `sector_id`, `date`, `indicator_id`
2. **Caching:** Don't remove 1-hour cache from expensive endpoints
3. **Data ingestion:** Run `data:ingest` daily (scheduled via `solid_queue`)
4. **Frontend:** Dash auto-optimizes, but avoid fetching all data at once

---

## Troubleshooting

### "A server is already running"
```bash
docker compose down
rm backend/tmp/pids/server.pid
docker compose up -d
```

### "Database does not exist"
```bash
docker compose down -v  # Remove volumes
docker compose up -d
docker compose exec backend bin/rails db:create db:migrate db:seed
```

### "Port already in use"
```bash
# Find what's using port
lsof -i :8051
# Kill it or change docker-compose.yml
```

### "Stale cache"
```bash
docker compose exec backend bin/rails runner 'Rails.cache.clear'
docker compose restart backend
```

### Frontend shows loading spinner forever
- Check browser console for API errors
- Verify backend is running: `curl http://localhost:8051/api/v1/countries`
- Check frontend logs: `docker compose logs frontend`

---

## Code Style & Conventions

- **Ruby:** Follow Rails conventions (snake_case, models in `app/models/`, services in `app/services/`)
- **Python:** Follow PEP 8 (4 spaces, descriptive names)
- **Commits:** Use imperative mood ("Add feature", not "Added feature")
- **Branches:** Not used in this project (main only)

---

## Key Resources

- **Rails API:** https://guides.rubyonrails.org/api_app.html
- **Plotly Dash:** https://dash.plotly.com/
- **FRED API:** https://fred.stlouisfed.org/docs/api/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **This project:** See `PROJECT.md`, `STATUS.md`, `API_ENDPOINTS.md`
