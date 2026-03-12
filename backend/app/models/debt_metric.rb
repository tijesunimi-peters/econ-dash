class DebtMetric < ApplicationRecord
  belongs_to :country
  has_many :data_points, class_name: 'DebtDataPoint', dependent: :destroy

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
end
