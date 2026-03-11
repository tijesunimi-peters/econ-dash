class IngestDataJob < ApplicationJob
  queue_as :default

  def perform(indicator_id = nil)
    indicators = if indicator_id
      Indicator.where(id: indicator_id)
    else
      Indicator.all
    end

    indicators.find_each do |indicator|
      ingest_indicator(indicator)
    rescue => e
      Rails.logger.error("Failed to ingest #{indicator.source_series_id}: #{e.class}: #{e.message}")
    end
  end

  private

  def ingest_indicator(indicator)
    last_date = indicator.data_points.maximum(:date)
    start_date = last_date ? last_date + 1.day : 5.years.ago.to_date

    observations = fetch_observations(indicator, start_date)

    DataPoint.transaction do
      observations.each do |obs|
        indicator.data_points.find_or_initialize_by(date: obs[:date]).tap do |dp|
          dp.value = obs[:value]
          dp.save!
        end
      end
    end

    Rails.logger.info("Ingested #{observations.size} points for #{indicator.source_series_id}")
  end

  def fetch_observations(indicator, start_date)
    case indicator.source
    when "FRED"
      FredClient.new.fetch_series(indicator.source_series_id, start_date: start_date)
    when "StatCan"
      StatcanClient.new.fetch_vector(indicator.source_series_id, start_date: start_date)
    when "BankOfCanada"
      BankOfCanadaClient.new.fetch_series(indicator.source_series_id, start_date: start_date)
    else
      Rails.logger.warn("Unknown source: #{indicator.source}")
      []
    end
  end
end
