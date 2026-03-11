class BusinessCycleService
  CONFIG_PATH = Rails.root.join("config", "indicator_classifications.yml")
  MOVING_AVG_WINDOW = 12

  def initialize(country)
    @country = country
    @config = load_config
  end

  def call
    leading_series_ids = @config.dig(country_code, "leading") || []
    inverted_ids = @config.dig(country_code, "inverted") || []
    sector_cycle_map = @config.dig(country_code, "sector_cycle_map") || {}

    leading_indicators = Indicator.where(source_series_id: leading_series_ids)
      .includes(:data_points)

    return empty_result if leading_indicators.empty?

    # Build composite leading index
    composite_index = compute_composite_index(leading_indicators, inverted_ids)
    return empty_result if composite_index.size < MOVING_AVG_WINDOW + 2

    # Detect cycle phase
    current_phase = detect_phase(composite_index)
    phase_duration = compute_phase_duration(composite_index)

    # Sector recommendations based on current phase
    recommended_sectors = sector_cycle_map[current_phase] || []

    # Leading indicators summary
    leading_summary = leading_indicators.map do |ind|
      accel = AccelerationService.new(ind).call
      latest = ind.data_points.order(:date).last
      {
        name: ind.name,
        source_series_id: ind.source_series_id,
        current_value: latest&.value&.to_f,
        direction: accel[:direction],
        rate_of_change: accel[:rate_of_change],
        inverted: inverted_ids.include?(ind.source_series_id),
      }
    end

    {
      composite_index: composite_index.last(60).map { |ci| { date: ci[:date], value: ci[:value].round(2) } },
      current_phase: current_phase,
      phase_duration_months: phase_duration,
      sector_recommendations: recommended_sectors,
      leading_indicators_summary: leading_summary,
    }
  end

  private

  def country_code
    @country.code.downcase
  end

  def load_config
    @loaded_config ||= YAML.load_file(CONFIG_PATH)
  end

  def compute_composite_index(indicators, inverted_ids)
    # Gather all monthly symmetric % changes per indicator
    all_changes = {}
    indicators.each do |ind|
      points = ind.data_points.order(:date).to_a
      next if points.size < 3

      changes = []
      points.each_cons(2) do |prev, curr|
        denom = curr.value.to_f + prev.value.to_f
        next if denom == 0

        sym_change = 200.0 * (curr.value.to_f - prev.value.to_f) / denom
        sym_change = -sym_change if inverted_ids.include?(ind.source_series_id)
        changes << { date: curr.date, value: sym_change }
      end

      # Compute historical std dev for normalization
      vals = changes.map { |c| c[:value] }
      std = standard_deviation(vals)
      next if std == 0

      # Normalize
      normalized = changes.map { |c| { date: c[:date], value: c[:value] / std } }
      all_changes[ind.id] = normalized
    end

    return [] if all_changes.empty?

    # Align by date and sum normalized changes
    date_sums = Hash.new { |h, k| h[k] = { total: 0.0, count: 0 } }
    all_changes.each_value do |series|
      series.each do |point|
        month_key = point[:date].beginning_of_month
        date_sums[month_key][:total] += point[:value]
        date_sums[month_key][:count] += 1
      end
    end

    # Only include dates where we have at least half the indicators
    min_count = [all_changes.size / 2, 1].max
    monthly_changes = date_sums
      .select { |_, v| v[:count] >= min_count }
      .sort_by { |date, _| date }
      .map { |date, v| { date: date, value: v[:total] } }

    # Cumulate into index (base = 100)
    cumulative = []
    index_value = 100.0
    monthly_changes.each do |mc|
      index_value += mc[:value]
      cumulative << { date: mc[:date], value: index_value }
    end

    cumulative
  end

  def detect_phase(composite_index)
    return "unknown" if composite_index.size < MOVING_AVG_WINDOW + 2

    values = composite_index.map { |ci| ci[:value] }
    current = values.last
    previous = values[-2]
    ma = values.last(MOVING_AVG_WINDOW).sum / MOVING_AVG_WINDOW

    rising = current > previous
    above_ma = current > ma

    if rising && above_ma
      "expansion"
    elsif !rising && above_ma
      "peak"
    elsif !rising && !above_ma
      "contraction"
    else # rising && !above_ma
      "trough"
    end
  end

  def compute_phase_duration(composite_index)
    return 0 if composite_index.size < MOVING_AVG_WINDOW + 2

    current_phase = detect_phase(composite_index)
    count = 0

    # Walk backwards through the index checking phase at each point
    (MOVING_AVG_WINDOW + 1...composite_index.size).to_a.reverse.each do |i|
      window = composite_index[0..i]
      phase = detect_phase(window)
      break if phase != current_phase
      count += 1
    end

    [count, 1].max
  end

  def standard_deviation(values)
    return 0.0 if values.size < 2
    mean = values.sum / values.size
    variance = values.sum { |v| (v - mean)**2 } / values.size
    Math.sqrt(variance)
  end

  def empty_result
    {
      composite_index: [],
      current_phase: "insufficient_data",
      phase_duration_months: 0,
      sector_recommendations: [],
      leading_indicators_summary: [],
    }
  end
end
