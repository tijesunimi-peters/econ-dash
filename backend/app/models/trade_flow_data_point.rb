class TradeFlowDataPoint < ApplicationRecord
  belongs_to :trade_flow

  validates :date, :value, presence: true
end
