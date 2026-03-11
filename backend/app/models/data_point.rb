class DataPoint < ApplicationRecord
  belongs_to :indicator

  validates :date, presence: true
  validates :value, presence: true
  validates :date, uniqueness: { scope: :indicator_id }
end
