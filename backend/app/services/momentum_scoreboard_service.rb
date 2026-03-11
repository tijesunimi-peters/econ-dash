class MomentumScoreboardService
  # Composite score weights
  YOY_WEIGHT = 0.40
  RATE_WEIGHT = 0.35
  TREND_WEIGHT = 0.25

  # Normalization cap for score components
  MAX_COMPONENT = 100.0

  def initialize(country)
    @country = country
  end

  def call
    sectors_data = SectorSummaryService.new(@country).call
    sectors = @country.sectors.includes(sub_industries: { indicators: :data_points })

    scored = sectors_data.map do |sector_summary|
      sector = sectors.find { |s| s.id == sector_summary[:id] }
      next unless sector

      acceleration_data = compute_sector_acceleration(sector)

      yoy = sector_summary[:yoy_change_pct] || 0.0
      rate_3m = acceleration_data[:avg_rate_of_change]
      trend_score = trend_to_score(sector_summary[:trend_direction])

      # Normalize each component to -100..+100 range
      yoy_normalized = clamp(yoy * 2, -MAX_COMPONENT, MAX_COMPONENT)
      rate_normalized = clamp(rate_3m * 5, -MAX_COMPONENT, MAX_COMPONENT)
      trend_normalized = trend_score * MAX_COMPONENT

      composite = (
        yoy_normalized * YOY_WEIGHT +
        rate_normalized * RATE_WEIGHT +
        trend_normalized * TREND_WEIGHT
      ).round(1)

      {
        sector_id: sector_summary[:id],
        sector_name: sector_summary[:name],
        composite_score: clamp(composite, -100, 100),
        yoy_change_pct: yoy.round(2),
        rate_of_change_3m: rate_3m.round(2),
        trend_direction: sector_summary[:trend_direction],
        acceleration_direction: acceleration_data[:direction],
        indicator_count: sector_summary[:indicator_count],
      }
    end.compact

    # Rank by composite score
    ranked = scored.sort_by { |s| -s[:composite_score] }
    ranked.each_with_index { |s, i| s[:rank] = i + 1 }

    ranked
  end

  private

  def compute_sector_acceleration(sector)
    accel_results = sector.indicators.map { |ind| AccelerationService.new(ind).call }
    valid = accel_results.select { |r| r[:rate_of_change].present? }

    if valid.any?
      avg_rate = valid.sum { |r| r[:rate_of_change] } / valid.size
      avg_accel = valid.sum { |r| r[:acceleration] } / valid.size

      direction_counts = valid.group_by { |r| r[:direction] }.transform_values(&:size)
      dominant_direction = direction_counts.max_by { |_, count| count }&.first || "stable"

      { avg_rate_of_change: avg_accel, direction: dominant_direction }
    else
      { avg_rate_of_change: 0.0, direction: "insufficient_data" }
    end
  end

  def trend_to_score(direction)
    case direction
    when "up" then 1.0
    when "down" then -1.0
    else 0.0
    end
  end

  def clamp(value, min, max)
    [[value, min].max, max].min
  end
end
