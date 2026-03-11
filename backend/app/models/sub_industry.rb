class SubIndustry < ApplicationRecord
  belongs_to :sector
  has_many :indicators, dependent: :destroy
  has_many :data_points, through: :indicators

  validates :name, presence: true
end
