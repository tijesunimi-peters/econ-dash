class IngestStructuralDataJob < ApplicationJob
  queue_as :default

  def perform
    puts "[IngestStructuralDataJob] Starting ingestion at #{Time.current}"

    begin
      client = WorldBankClient.new
      countries = Country.where(code: ["US", "CA", "JP", "AU", "DE"])
      failed = []
      successful = 0

      countries.each do |country|
        puts "Ingesting #{country.name}..."

        WorldBankClient::INDICATORS.each do |metric_type, wb_code|
          begin
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

      puts "[IngestStructuralDataJob] Completed: #{successful} successful, #{failed.length} failed"

      # Log the ingest result
      DataIngestLog.create!(
        data_type: "structural",
        status: "success",
        records_processed: successful,
        completed_at: Time.current
      )
    rescue => e
      puts "[IngestStructuralDataJob] Failed: #{e.message}"

      DataIngestLog.create!(
        data_type: "structural",
        status: "failed",
        error_message: e.message,
        completed_at: Time.current
      )

      raise
    end
  end
end
