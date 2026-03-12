class StructuralDataPoint < ApplicationRecord
  belongs_to :structural_metric

  validates :date, :value, presence: true
end
