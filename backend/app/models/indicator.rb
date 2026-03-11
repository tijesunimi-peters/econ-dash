class Indicator < ApplicationRecord
  belongs_to :sub_industry
  has_many :data_points, dependent: :destroy

  validates :name, presence: true
  validates :source, presence: true
  validates :source_series_id, presence: true, uniqueness: true
end
