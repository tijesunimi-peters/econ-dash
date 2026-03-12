class IngestDebtDataJob < ApplicationJob
  queue_as :default

  def perform
    puts "[IngestDebtDataJob] Starting ingestion at #{Time.current}"

    begin
      client = WorldBankClient.new
      countries = Country.where(code: ["US", "CA", "JP", "AU", "DE"])
      failed = []
      successful = 0

      countries.each do |country|
        puts "Ingesting #{country.name}..."

        WorldBankClient::DEBT_INDICATORS.each do |metric_type, wb_code|
          begin
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
                successful += 1
              end
            end

            sleep 0.5  # Rate limiting
          rescue => e
            puts "Error: #{e.message}"
            failed << "#{country.code} #{metric_type_str}"
          end
        end
      end

      puts "[IngestDebtDataJob] Completed: #{successful} successful, #{failed.length} failed"

      # Log the ingest result
      DataIngestLog.create!(
        data_type: "debt",
        status: "success",
        records_processed: successful,
        completed_at: Time.current
      )
    rescue => e
      puts "[IngestDebtDataJob] Failed: #{e.message}"

      DataIngestLog.create!(
        data_type: "debt",
        status: "failed",
        error_message: e.message,
        completed_at: Time.current
      )

      raise
    end
  end
end
