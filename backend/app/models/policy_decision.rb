# Policy Decision Model
# Tracks central bank rate decisions, government fiscal policy, regulations, tariffs, etc.
#
# Examples:
#   PolicyDecision.create!(
#     country: Country.find_by(code: 'us'),
#     decision_type: 'interest_rate',
#     announcement_date: Date.parse('2026-03-12'),
#     effective_date: Date.parse('2026-03-15'),
#     description: 'Federal Reserve raises rates 25bps to 5.50%',
#     impact_sectors: ['Financial', 'Consumer', 'Real Estate'],
#     expected_lag_months: 1,
#     status: 'effective',
#     source: 'Federal Reserve FOMC Statement'
#   )

class PolicyDecision < ApplicationRecord
  belongs_to :country

  DECISION_TYPES = [
    'interest_rate',    # Central bank rate decisions
    'qe',               # Quantitative easing / quantitative tightening
    'regulation',       # New regulations affecting sectors
    'tariff',           # Trade tariffs / trade policies
    'stimulus',         # Fiscal stimulus measures
    'subsidy',          # Government subsidies
    'tax',              # Tax policy changes
    'infrastructure'    # Infrastructure spending
  ].freeze

  STATUSES = [
    'announced',  # Policy announced but not yet effective
    'effective',  # Policy is currently in effect
    'completed',  # Policy has ended
    'reversed'    # Policy was reversed / withdrawn
  ].freeze

  validates :country_id, presence: true
  validates :decision_type, presence: true, inclusion: { in: DECISION_TYPES }
  validates :announcement_date, presence: true
  validates :effective_date, presence: true
  validates :description, presence: true
  validates :status, presence: true, inclusion: { in: STATUSES }
  validates :impact_sectors, presence: true
  validates :expected_lag_months, numericality: { only_integer: true, greater_than_or_equal_to: 0 }

  # Scopes
  scope :by_country, ->(country_id) { where(country_id: country_id) }
  scope :recent, -> { order(announcement_date: :desc) }
  scope :active, -> { where(status: ['announced', 'effective']) }
  scope :by_type, ->(type) { where(decision_type: type) }
  scope :since, ->(date) { where('announcement_date >= ?', date) }

  # Check if policy is currently active
  def active?
    status.in?(['announced', 'effective'])
  end

  # Calculate when policy impact should show in economic data
  def expected_impact_date
    effective_date + expected_lag_months.months
  end

  # Human-readable decision type
  def decision_type_label
    decision_type.titleize
  end
end
