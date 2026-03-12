# Market Sentiment Model
# Tracks market expectations and sentiment indicators
#
# Examples:
#   MarketSentiment.create!(
#     country: Country.find_by(code: 'us'),
#     metric_type: 'fed_rate_expectations',
#     value: 5.00,  # Market expects 5.00% by end of year
#     date: Date.today,
#     source: 'CME FedWatch Tool',
#     trend: 'stable',
#     unit: '%',
#     prior_value: 4.75,
#     notes: 'Based on 30-day futures pricing'
#   )

class MarketSentiment < ApplicationRecord
  belongs_to :country

  METRIC_TYPES = [
    'cci',                      # Consumer Confidence Index
    'pmi',                      # Manufacturing PMI
    'services_pmi',             # Services PMI
    'vix',                      # Volatility Index
    'fed_rate_expectations',    # Market expectations for Fed rates
    'inflation_expectations',   # Market expectations for inflation
    'yield_curve_2_10',        # 2Y-10Y yield spread
    'credit_spreads',          # Bond credit spreads
    'usd_index',               # US Dollar Index
    'unemployment_expectations' # Forecast unemployment rate
  ].freeze

  TRENDS = ['up', 'down', 'stable'].freeze

  validates :country_id, presence: true
  validates :metric_type, presence: true, inclusion: { in: METRIC_TYPES }
  validates :value, presence: true, numericality: true
  validates :date, presence: true
  validates :trend, inclusion: { in: TRENDS }, allow_nil: true
  validates :unit, presence: true

  scope :by_country, ->(country_id) { where(country_id: country_id) }
  scope :by_metric, ->(metric_type) { where(metric_type: metric_type) }
  scope :recent, -> { order(date: :desc) }
  scope :since, ->(date) { where('date >= ?', date) }
  scope :latest_by_metric, -> {
    select('DISTINCT ON (metric_type) *').order('metric_type, date DESC')
  }

  # Calculate change from prior value
  def change_from_prior
    return nil unless prior_value.present?
    value - prior_value
  end

  # Calculate percent change
  def percent_change_from_prior
    return nil unless prior_value.present? && prior_value != 0
    ((value - prior_value) / prior_value * 100).round(2)
  end

  # Human-readable metric name
  def metric_label
    case metric_type
    when 'cci'
      'Consumer Confidence Index'
    when 'pmi'
      'Manufacturing PMI'
    when 'services_pmi'
      'Services PMI'
    when 'vix'
      'VIX (Volatility Index)'
    when 'fed_rate_expectations'
      'Fed Rate Expectations'
    when 'inflation_expectations'
      'Inflation Expectations'
    when 'yield_curve_2_10'
      'Yield Curve (2Y-10Y)'
    when 'credit_spreads'
      'Credit Spreads'
    when 'usd_index'
      'US Dollar Index'
    when 'unemployment_expectations'
      'Unemployment Expectations'
    else
      metric_type.titleize
    end
  end

  # Interpretation helper
  def sentiment_interpretation
    case metric_type
    when 'pmi', 'services_pmi'
      value > 50 ? 'Expansion' : 'Contraction'
    when 'cci'
      value > 100 ? 'Confident' : 'Cautious'
    when 'vix'
      value < 20 ? 'Low Volatility' : (value < 30 ? 'Moderate' : 'High Volatility')
    when 'yield_curve_2_10'
      value > 0 ? 'Normal Upward Slope' : 'Inverted (Recession Warning)'
    else
      nil
    end
  end
end
