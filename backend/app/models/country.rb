class Country < ApplicationRecord
  has_many :sectors, dependent: :destroy

  validates :name, presence: true
  validates :code, presence: true, uniqueness: true
end
