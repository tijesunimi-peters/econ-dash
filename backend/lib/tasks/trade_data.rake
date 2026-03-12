namespace :trade_data do
  desc "Ingest trade flow metrics from World Bank API (last 5 years)"
  task ingest: :environment do
    puts "Starting trade flow data ingestion from World Bank..."
    failed = []
    successful = 0

    client = WorldBankClient.new
    countries = Country.where(code: ["US", "CA", "JP", "AU", "DE"])

    # Map TradeFlow types to World Bank indicator codes
    flow_types = {
      'exports_pct_gdp' => 'NE.EXP.GNFS.CD.ZS',        # Exports of goods and services (% of GDP)
      'imports_pct_gdp' => 'NE.IMP.GNFS.CD.ZS',        # Imports of goods and services (% of GDP)
      'fdi_inflows_pct_gdp' => 'BX.KLT.DINV.GD.ZS'    # FDI inflows (% of GDP)
    }

    countries.each do |country|
      puts "\n=== Ingesting #{country.name} (#{country.code}) ==="

      flow_types.each do |flow_type, wb_code|
        begin
          puts "  Fetching #{flow_type} (#{wb_code}) for #{country.code}..."
          data_points = client.fetch_indicator(wb_code, country.code)

          if data_points.empty?
            puts "    No data available"
            next
          end

          TradeFlow.transaction do
            # Find or create the trade flow record
            metric = country.trade_flows.find_or_initialize_by(
              flow_type: flow_type,
              date: Date.today
            )

            # Set metadata
            metric.unit = TradeFlow::FLOW_TYPES[flow_type][:unit]
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
          failed << "#{country.code} #{flow_type}"
        end
      end
    end

    puts "\n=== Summary ==="
    puts "Successful ingestions: #{successful}"
    puts "Total TradeFlow records: #{TradeFlow.count}"
    puts "Total TradeFlowDataPoint records: #{TradeFlowDataPoint.count}"
    puts "Failed (#{failed.size}): #{failed.join(', ')}" if failed.any?
  end
end
