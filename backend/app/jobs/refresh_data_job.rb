class RefreshDataJob < ApplicationJob
  queue_as :default

  def perform(country_id)
    country = Country.find(country_id)
    puts "[RefreshDataJob] Starting refresh for #{country.name} at #{Time.current}"

    begin
      successful_types = []
      failed_types = []

      # Refresh indicator data (FRED, StatCan, BankOfCanada) via sub-industries
      begin
        refresh_indicator_data_for_country(country)
        successful_types << "indicators"
        puts "[RefreshDataJob] Completed indicator refresh for #{country.name}"
      rescue => e
        Rails.logger.error("[RefreshDataJob] Failed to refresh indicators for #{country.name}: #{e.message}")
        failed_types << "indicators"
      end

      # Refresh structural metrics (World Bank)
      begin
        refresh_structural_metrics_for_country(country)
        successful_types << "structural"
        puts "[RefreshDataJob] Completed structural refresh for #{country.name}"
      rescue => e
        Rails.logger.error("[RefreshDataJob] Failed to refresh structural metrics for #{country.name}: #{e.message}")
        failed_types << "structural"
      end

      # Refresh debt metrics (World Bank)
      begin
        refresh_debt_metrics_for_country(country)
        successful_types << "debt"
        puts "[RefreshDataJob] Completed debt refresh for #{country.name}"
      rescue => e
        Rails.logger.error("[RefreshDataJob] Failed to refresh debt metrics for #{country.name}: #{e.message}")
        failed_types << "debt"
      end

      # Log the structural and debt refresh results (DataIngestLog only tracks these)
      ["structural", "debt"].each do |data_type|
        if successful_types.include?(data_type)
          DataIngestLog.create!(
            data_type: data_type,
            status: "success",
            records_processed: 1,
            completed_at: Time.current
          )
        elsif failed_types.include?(data_type)
          DataIngestLog.create!(
            data_type: data_type,
            status: "failed",
            error_message: "Refresh failed for #{country.name}",
            completed_at: Time.current
          )
        end
      end

      puts "[RefreshDataJob] Completed for #{country.name}: #{successful_types.length} successful, #{failed_types.length} failed"
    rescue => e
      puts "[RefreshDataJob] Failed for #{country.name}: #{e.message}"
      raise
    end
  end

  private

  def refresh_indicator_data_for_country(country)
    # Get all indicators for this country's sub-industries
    indicators = Indicator.joins(sub_industry: { sector: :country })
      .where(countries: { id: country.id })
      .distinct

    indicators.find_each do |indicator|
      IngestDataJob.perform_now(indicator.id)
    end
  end

  private

  def refresh_structural_metrics_for_country(country)
    client = WorldBankClient.new

    WorldBankClient::INDICATORS.each do |metric_type, wb_code|
      metric_type_str = metric_type.to_s
      data_points = client.fetch_indicator(wb_code, country.code)

      next if data_points.empty?

      StructuralMetric.transaction do
        metric = country.structural_metrics.find_or_initialize_by(
          metric_type: metric_type_str,
          date: Date.today
        )

        metric.unit = StructuralMetric::METRIC_TYPES[metric_type_str][:unit]
        metric.source = "world_bank"

        latest = data_points.max_by { |dp| dp[:date] }

        if latest
          metric.value = latest[:value]
          metric.date = latest[:date]
          metric.save!

          data_points.each do |point|
            metric.data_points.find_or_initialize_by(date: point[:date]).tap do |dp|
              dp.value = point[:value]
              dp.save!
            end
          end
        end
      end

      sleep 0.5  # Rate limiting
    end
  end

  def refresh_debt_metrics_for_country(country)
    client = WorldBankClient.new

    WorldBankClient::DEBT_INDICATORS.each do |metric_type, wb_code|
      metric_type_str = metric_type.to_s
      data_points = client.fetch_indicator(wb_code, country.code)

      next if data_points.empty?

      DebtMetric.transaction do
        metric = country.debt_metrics.find_or_initialize_by(
          metric_type: metric_type_str,
          date: Date.today
        )

        metric.unit = DebtMetric::METRIC_TYPES[metric_type_str][:unit]
        metric.source = "world_bank"

        latest = data_points.max_by { |dp| dp[:date] }

        if latest
          metric.value = latest[:value]
          metric.date = latest[:date]

          data_points.each do |point|
            metric.data_points.find_or_initialize_by(date: point[:date]).tap do |dp|
              dp.value = point[:value]
              dp.save!
            end
          end

          # Calculate trend
          sorted = data_points.sort_by { |dp| dp[:date] }
          first_val = sorted.first[:value].to_f
          last_val = sorted.last[:value].to_f
          pct_change = ((last_val - first_val) / first_val * 100) rescue nil

          metric.trend = if pct_change.nil?
            "stable"
          elsif pct_change <= -1.0
            "down"
          elsif pct_change >= 1.0
            "up"
          else
            "stable"
          end

          metric.save!
        end
      end

      sleep 0.5  # Rate limiting
    end
  end
end
