namespace :debt_data do
  desc "Ingest debt metrics from World Bank API (last 5 years)"
  task ingest: :environment do
    puts "Starting debt data ingestion from World Bank..."
    failed = []
    successful = 0

    client = WorldBankClient.new
    countries = Country.where(code: ["US", "CA", "JP", "AU", "DE"])

    countries.each do |country|
      puts "\n=== Ingesting #{country.name} (#{country.code}) ==="

      WorldBankClient::DEBT_INDICATORS.each do |metric_type, wb_code|
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

          DebtMetric.transaction do
            # Find or create the debt metric record
            metric = country.debt_metrics.find_or_initialize_by(
              metric_type: metric_type_str,
              date: Date.today
            )

            # Set metadata
            metric.unit = DebtMetric::METRIC_TYPES[metric_type_str][:unit]
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

              # Calculate and save trend
              metric.trend = calculate_trend(data_points)
              metric.save!

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
    puts "Total DebtMetric records: #{DebtMetric.count}"
    puts "Total DebtDataPoint records: #{DebtDataPoint.count}"
    puts "Failed (#{failed.size}): #{failed.join(', ')}" if failed.any?
  end

  private

  def calculate_trend(data_points)
    return "stable" if data_points.length < 2

    sorted = data_points.sort_by { |dp| dp[:date] }
    first_val = sorted.first[:value].to_f
    last_val = sorted.last[:value].to_f
    pct_change = ((last_val - first_val) / first_val * 100) rescue nil

    return "stable" if pct_change.nil?

    case pct_change
    when (-Float::INFINITY)..-1.0 then "down"
    when 1.0..Float::INFINITY then "up"
    else "stable"
    end
  end
end
