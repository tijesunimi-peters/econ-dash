namespace :data do
  desc "Ingest economic data from all sources (last 5 years for new indicators)"
  task ingest: :environment do
    failed = []

    Indicator.find_each do |indicator|
      last_date = indicator.data_points.maximum(:date)
      start_date = last_date ? last_date + 1.day : 5.years.ago.to_date

      puts "Ingesting #{indicator.source_series_id} (#{indicator.source}) from #{start_date}..."

      observations = fetch_with_retry(indicator, start_date)

      DataPoint.transaction do
        observations.each do |obs|
          indicator.data_points.find_or_initialize_by(date: obs[:date]).tap do |dp|
            dp.value = obs[:value]
            dp.save!
          end
        end
      end

      puts "  Saved #{observations.size} data points"
      sleep 0.5 # rate limit courtesy
    rescue => e
      puts "  ERROR: #{e.class}: #{e.message}"
      failed << indicator.source_series_id
    end

    puts "\nDone. Total data points: #{DataPoint.count}"
    puts "Failed (#{failed.size}): #{failed.join(', ')}" if failed.any?
  end
end

def fetch_with_retry(indicator, start_date, retries: 3)
  attempts = 0
  begin
    attempts += 1
    case indicator.source
    when "FRED"
      FredClient.new.fetch_series(indicator.source_series_id, start_date: start_date)
    when "StatCan"
      StatcanClient.new.fetch_vector(indicator.source_series_id, start_date: start_date)
    when "BankOfCanada"
      BankOfCanadaClient.new.fetch_series(indicator.source_series_id, start_date: start_date)
    else
      []
    end
  rescue RuntimeError => e
    if attempts < retries && e.message.match?(/50[0-9]/)
      puts "  Retry #{attempts}/#{retries} after error: #{e.message}"
      sleep(2 * attempts)
      retry
    else
      raise
    end
  end
end
