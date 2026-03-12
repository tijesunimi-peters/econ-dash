class TradeFlow < ApplicationRecord
  belongs_to :country
  has_many :data_points, class_name: 'TradeFlowDataPoint', dependent: :destroy

  FLOW_TYPES = {
    # Trade balance & volumes
    'exports_pct_gdp' => { label: 'Exports (% of GDP)', unit: '% of GDP', category: 'volumes' },
    'imports_pct_gdp' => { label: 'Imports (% of GDP)', unit: '% of GDP', category: 'volumes' },
    'trade_balance_pct_gdp' => { label: 'Trade Balance (% of GDP)', unit: '% of GDP', category: 'balance' },

    # Foreign Investment
    'fdi_inflows_pct_gdp' => { label: 'FDI Inflows (% of GDP)', unit: '% of GDP', category: 'investment' },

    # Supply Chain Risk
    'supply_chain_concentration' => { label: 'Supply Chain Concentration', unit: 'index', category: 'risk' },
    'export_diversification' => { label: 'Export Diversification', unit: 'index', category: 'resilience' },
    'import_dependency_ratio' => { label: 'Import Dependency Ratio', unit: 'ratio', category: 'vulnerability' }
  }.freeze

  validates :flow_type, presence: true, inclusion: { in: FLOW_TYPES.keys }
  validates :value, presence: true, numericality: true
  validates :date, :country_id, :unit, presence: true

  scope :by_country, ->(country_id) { where(country_id: country_id) }
  scope :by_flow_type, ->(flow_type) { where(flow_type: flow_type) }
  scope :recent, -> { order(date: :desc).limit(30) }
  scope :since, ->(date) { where('date >= ?', date) }

  def metric_label
    FLOW_TYPES[flow_type]&.fetch(:label, flow_type.humanize)
  end

  def category
    FLOW_TYPES[flow_type]&.fetch(:category, 'other')
  end

  def alert_level
    return 'none' unless value.present?

    case flow_type
    when 'supply_chain_concentration'
      value > 40 ? 'critical' : value > 30 ? 'warning' : 'none'
    when 'import_dependency_ratio'
      value > 2.0 ? 'critical' : value > 1.5 ? 'warning' : 'none'
    when 'exports_pct_gdp'
      # Very low exports < 10% may indicate trade isolation
      value < 10 ? 'warning' : 'none'
    when 'imports_pct_gdp'
      # Very high imports > 50% may indicate trade dependency
      value > 50 ? 'warning' : 'none'
    when 'fdi_inflows_pct_gdp'
      # Low FDI < 1% may indicate investment gap
      value < 1 ? 'warning' : 'none'
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
