namespace :structural_data do
  desc "Ingest structural metrics from World Bank API (last 5 years)"
  task ingest: :environment do
    puts "Starting structural data ingestion from World Bank..."
    failed = []
    successful = 0

    client = WorldBankClient.new
    countries = Country.where(code: ["US", "CA", "JP", "AU", "DE"])

    countries.each do |country|
      puts "\n=== Ingesting #{country.name} (#{country.code}) ==="

      WorldBankClient::INDICATORS.each do |metric_type, wb_code|
        begin
          metric_type_str = metric_type.to_s  # Convert symbol to string
          puts "  Fetching #{metric_type_str} (#{wb_code}) for #{country.code}..."
          data_points = client.fetch_indicator(wb_code, country.code)
          puts "    Got #{data_points.class} with #{data_points.length} items"
          puts "    First item: #{data_points.first.inspect}" if data_points.any?

          if data_points.empty?
            puts "    No data available"
            next
          end

          StructuralMetric.transaction do
            # Find or create the structural metric record
            metric = country.structural_metrics.find_or_initialize_by(
              metric_type: metric_type_str,
              date: Date.today
            )

            # Set metadata
            metric.unit = StructuralMetric::METRIC_TYPES[metric_type_str][:unit]
            metric.source = "world_bank"

            # Use the most recent data point as the current value
            latest = data_points.max_by { |dp| dp[:date] }

            if latest
              metric.value = latest[:value]
              metric.date = latest[:date]

              metric.save!

              # Save all historical data points
              data_points.each do |point|
                metric.data_points.find_or_initialize_by(date: point[:date]).tap do |dp|
                  dp.value = point[:value]
                  dp.save!
                end
              end

              puts "    Saved #{data_points.size} data points (latest: #{latest[:value]} on #{latest[:date]})"
              successful += 1
            else
              puts "    ERROR: No valid data points found"
            end
          end

          sleep 0.5  # Rate limiting
        rescue => e
          puts "    ERROR: #{e.class}: #{e.message}"
          failed << "#{country.code} #{metric_type_str}"
        end
      end
    end

    puts "\n=== Summary ==="
    puts "Successful ingestions: #{successful}"
    puts "Total StructuralMetric records: #{StructuralMetric.count}"
    puts "Total StructuralDataPoint records: #{StructuralDataPoint.count}"
    puts "Failed (#{failed.size}): #{failed.join(', ')}" if failed.any?
  end
end
