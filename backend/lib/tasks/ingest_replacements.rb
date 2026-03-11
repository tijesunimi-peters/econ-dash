%w[CANSLRTTO01GPSAM COCANZ21].each do |series_id|
  ind = Indicator.find_by(source_series_id: series_id)
  next unless ind
  begin
    observations = FredClient.new.fetch_series(series_id, start_date: 5.years.ago.to_date)
    observations.each do |obs|
      dp = ind.data_points.find_or_initialize_by(date: obs[:date])
      dp.value = obs[:value]
      dp.save!
    end
    puts "#{series_id}: saved #{observations.size} points"
  rescue => e
    puts "#{series_id}: ERROR #{e.message}"
  end
  sleep 2
end
puts "Total: #{DataPoint.count}"
