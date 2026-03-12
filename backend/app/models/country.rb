class Country < ApplicationRecord
  has_many :sectors, dependent: :destroy
  has_many :policy_decisions, dependent: :destroy

  validates :name, presence: true
  validates :code, presence: true, uniqueness: true
end
