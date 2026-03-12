class DataIngestLog < ApplicationRecord
  validates :data_type, presence: true, inclusion: { in: ["structural", "debt"] }
  validates :status, presence: true, inclusion: { in: ["success", "failed"] }

  scope :recent, -> { order(completed_at: :desc).limit(10) }
  scope :by_type, ->(type) { where(data_type: type) }
  scope :successful, -> { where(status: "success") }
  scope :failed, -> { where(status: "failed") }

  def self.last_success(data_type)
    by_type(data_type).successful.first
  end

  def self.last_failure(data_type)
    by_type(data_type).failed.first
  end
end
