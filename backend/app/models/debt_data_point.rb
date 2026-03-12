class DebtDataPoint < ApplicationRecord
  belongs_to :debt_metric

  validates :date, :value, presence: true
end
