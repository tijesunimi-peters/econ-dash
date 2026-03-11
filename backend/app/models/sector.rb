class Sector < ApplicationRecord
  belongs_to :country
  has_many :sub_industries, dependent: :destroy
  has_many :indicators, through: :sub_industries

  validates :name, presence: true
end
