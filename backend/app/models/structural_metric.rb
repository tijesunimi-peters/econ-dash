class StructuralMetric < ApplicationRecord
  belongs_to :country

  METRIC_TYPES = {
    'population' => { label: 'Population', unit: 'millions', category: 'demographics' },
    'median_age' => { label: 'Median Age', unit: 'years', category: 'demographics' },
    'labor_participation' => { label: 'Labor Force Participation', unit: '%', category: 'demographics' },
    'life_expectancy' => { label: 'Life Expectancy', unit: 'years', category: 'demographics' },
    'tfp_growth' => { label: 'Total Factor Productivity Growth', unit: '%', category: 'productivity' },
    'rd_pct_gdp' => { label: 'R&D Spending', unit: '% of GDP', category: 'productivity' },
    'education_spending_pct_gdp' => { label: 'Education Spending', unit: '% of GDP', category: 'productivity' }
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
    when 'median_age'
      value >= 45 ? 'critical' : value >= 43 ? 'warning' : 'none'
    when 'labor_participation'
      value < 60 ? 'critical' : value < 65 ? 'warning' : 'none'
    when 'population'
      # Population growth < 0.5% is warning
      value < 0.5 ? 'warning' : 'none'
    when 'life_expectancy'
      value < 75 ? 'warning' : 'none'
    when 'tfp_growth'
      value < 1.0 ? 'warning' : 'none'
    when 'rd_pct_gdp'
      value < 1.5 ? 'warning' : 'none'
    when 'education_spending_pct_gdp'
      value < 4.0 ? 'warning' : 'none'
    else
      'none'
    end
  end
end
