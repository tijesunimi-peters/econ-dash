class DebtMetric < ApplicationRecord
  belongs_to :country

  METRIC_TYPES = {
    'govt_debt_pct_gdp' => { label: 'Government Debt', unit: '% of GDP', category: 'government' },
    'corp_debt_ratio' => { label: 'Corporate Debt Ratio', unit: 'ratio', category: 'corporate' },
    'hhd_debt_pct_income' => { label: 'Household Debt', unit: '% of income', category: 'household' },
    'deficit_pct_gdp' => { label: 'Budget Deficit', unit: '% of GDP', category: 'government' }
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
  scope :latest_by_metric, -> {
    select('DISTINCT ON (metric_type) *')
      .order(metric_type: :asc, date: :desc)
  }

  def metric_label
    METRIC_TYPES[metric_type]&.fetch(:label, metric_type.humanize)
  end

  def category
    METRIC_TYPES[metric_type]&.fetch(:category, 'other')
  end

  def alert_level
    return 'none' unless value.present?

    case metric_type
    when 'govt_debt_pct_gdp'
      value >= 120 ? 'critical' : value >= 90 ? 'warning' : 'none'
    when 'corp_debt_ratio'
      value >= 4.0 ? 'critical' : value >= 3.0 ? 'warning' : 'none'
    when 'hhd_debt_pct_income'
      value >= 150 ? 'critical' : value >= 100 ? 'warning' : 'none'
    when 'deficit_pct_gdp'
      value >= 5.0 ? 'critical' : value >= 3.0 ? 'warning' : 'none'
    else
      'none'
    end
  end

  def trend_interpretation
    case trend
    when 'up'
      "Increasing - potential concern for sustainability"
    when 'down'
      "Decreasing - improving fiscal position"
    when 'stable'
      "Stable - consistent level"
    else
      nil
    end
  end
end
