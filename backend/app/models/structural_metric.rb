class StructuralMetric < ApplicationRecord
  belongs_to :country
  has_many :data_points, class_name: 'StructuralDataPoint', dependent: :destroy

  METRIC_TYPES = {
    # Demographics (Seed + World Bank)
    'population' => { label: 'Population', unit: 'millions', category: 'demographics' },
    'median_age' => { label: 'Median Age', unit: 'years', category: 'demographics' },
    'life_expectancy' => { label: 'Life Expectancy', unit: 'years', category: 'demographics' },
    'urban_population_pct' => { label: 'Urban Population', unit: '%', category: 'demographics' },

    # Labor & Employment (World Bank)
    'labor_participation' => { label: 'Labor Force Participation', unit: '%', category: 'labor' },

    # Productivity & Innovation (Seed + World Bank)
    'tfp_growth' => { label: 'Total Factor Productivity Growth', unit: '%', category: 'productivity' },
    'rd_pct_gdp' => { label: 'R&D Spending', unit: '% of GDP', category: 'productivity' },
    'manufacturing_value_added_pct' => { label: 'Manufacturing Output', unit: '% of GDP', category: 'productivity' },
    'service_sector_pct' => { label: 'Service Sector', unit: '% of GDP', category: 'productivity' },
    'education_spending_pct_gdp' => { label: 'Education Spending', unit: '% of GDP', category: 'productivity' },

    # Economic Development (World Bank)
    'gdp_per_capita' => { label: 'GDP per Capita', unit: 'USD', category: 'development' },
    'gdp_per_capita_growth' => { label: 'GDP per Capita Growth', unit: '%', category: 'development' },

    # Trade & Investment (World Bank)
    'foreign_direct_investment_pct' => { label: 'FDI Inflows', unit: '% of GDP', category: 'trade' },
    'merchandise_exports_pct_gdp' => { label: 'Merchandise Exports', unit: '% of GDP', category: 'trade' },
    'merchandise_imports_pct_gdp' => { label: 'Merchandise Imports', unit: '% of GDP', category: 'trade' }
  }.freeze

  validates :metric_type, presence: true, inclusion: { in: METRIC_TYPES.keys }
  validates :value, presence: true, numericality: true
  validates :date, presence: true
  validates :unit, presence: true
  validates :country_id, presence: true

  scope :by_country, ->(country_id) { where(country_id: country_id) }
  scope :by_metric, ->(metric_type) { where(metric_type: metric_type) }
  scope :recent, -> { order(date: :desc).limit(30) }
  scope :since, ->(date) { where('date >= ?', date) }

  def metric_label
    METRIC_TYPES[metric_type]&.fetch(:label, metric_type.humanize)
  end

  def category
    METRIC_TYPES[metric_type]&.fetch(:category, 'other')
  end

  def alert_level
    return 'none' unless value.present?

    case metric_type
    # Demographics
    when 'median_age'
      value >= 45 ? 'critical' : value >= 43 ? 'warning' : 'none'
    when 'life_expectancy'
      value < 75 ? 'warning' : 'none'
    when 'urban_population_pct'
      # Low urbanization < 30% may indicate underdevelopment
      value < 30 ? 'warning' : 'none'
    when 'population'
      # Population growth < 0.5% is warning
      value < 0.5 ? 'warning' : 'none'

    # Labor & Employment
    when 'labor_participation'
      value < 60 ? 'critical' : value < 65 ? 'warning' : 'none'

    # Productivity
    when 'tfp_growth'
      value < 1.0 ? 'warning' : 'none'
    when 'rd_pct_gdp'
      value < 1.5 ? 'warning' : 'none'
    when 'education_spending_pct_gdp'
      value < 4.0 ? 'warning' : 'none'
    when 'manufacturing_value_added_pct'
      # Low manufacturing < 10% may indicate vulnerability
      value < 10 ? 'warning' : 'none'
    when 'service_sector_pct'
      # Very high service dependency > 80% can indicate risk
      value > 80 ? 'warning' : 'none'

    # Economic Development
    when 'gdp_per_capita'
      # Low GDP per capita < $10k indicates lower development
      value < 10000 ? 'warning' : 'none'
    when 'gdp_per_capita_growth'
      # Negative growth or very low growth < 0.5% is warning
      value < 0.5 ? 'warning' : 'none'

    # Trade & Investment
    when 'foreign_direct_investment_pct'
      # Low FDI < 1% may indicate investment gap
      value < 1 ? 'warning' : 'none'
    when 'merchandise_exports_pct_gdp'
      # Very low exports < 10% may indicate trade isolation
      value < 10 ? 'warning' : 'none'
    when 'merchandise_imports_pct_gdp'
      # Very high imports > 50% may indicate trade dependency
      value > 50 ? 'warning' : 'none'

    else
      'none'
    end
  end

  # Calculate trend from historical data (last 5 years)
  def trend_5year
    historical = data_points
      .order(date: :asc)
      .last(5)

    return nil if historical.length < 2

    first_val = historical.first.value.to_f
    last_val = historical.last.value.to_f
    pct_change = ((last_val - first_val) / first_val * 100) rescue nil

    return nil if pct_change.nil?

    case pct_change
    when (-Float::INFINITY)..-1.0 then "down"
    when 1.0..Float::INFINITY then "up"
    else "stable"
    end
  end

  # Get historical data for sparklines (last N years)
  def historical_data(years: 5)
    cutoff_date = date - years.years
    data_points
      .where("date >= ?", cutoff_date)
      .order(date: :asc)
      .pluck(:date, :value)
      .map { |d, v| { date: d, value: v.to_f } }
  end

  # Generate forecast for future values
  # Returns forecast data with confidence intervals
  def forecast(periods: 2, method: :linear)
    hist_data = historical_data(years: 10)

    case method
    when :linear
      TrendForecastService.forecast_linear(hist_data, periods: periods)
    when :exponential
      TrendForecastService.forecast_exponential(hist_data, periods: periods)
    else
      TrendForecastService.forecast_linear(hist_data, periods: periods)
    end
  end
end
