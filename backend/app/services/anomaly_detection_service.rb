class AnomalyDetectionService
  ROLLING_WINDOW = 12 # months
  WARNING_THRESHOLD = 2.0
  CRITICAL_THRESHOLD = 3.0

  def initialize(country)
    @country = country
  end

  def call
    indicators = Indicator.joins(sub_industry: { sector: :country })
      .where(sectors: { country_id: @country.id })
      .includes(:data_points, sub_industry: :sector)

    anomalies = indicators.flat_map { |ind| detect_anomalies(ind) }.compact
    anomalies.sort_by { |a| -a[:z_score].abs }
  end

  private

  def detect_anomalies(indicator)
    points = indicator.data_points.sort_by(&:date)
    return [] if points.size < ROLLING_WINDOW + 1

    # Use last ROLLING_WINDOW+1 points to compute rolling stats and check latest
    recent = points.last(ROLLING_WINDOW + 1)
    rolling_values = recent[0...-1].map { |p| p.value.to_f }
    current_value = recent.last.value.to_f

    mean = rolling_values.sum / rolling_values.size
    variance = rolling_values.sum { |v| (v - mean)**2 } / rolling_values.size
    std_dev = Math.sqrt(variance)

    return [] if std_dev == 0

    z_score = (current_value - mean) / std_dev

    if z_score.abs >= WARNING_THRESHOLD
      severity = z_score.abs >= CRITICAL_THRESHOLD ? "critical" : "warning"

      [{
        indicator_id: indicator.id,
        indicator_name: indicator.name,
        sector_name: indicator.sub_industry.sector.name,
        sub_industry_name: indicator.sub_industry.name,
        current_value: current_value,
        rolling_mean: mean.round(4),
        rolling_std: std_dev.round(4),
        z_score: z_score.round(2),
        severity: severity,
        direction: z_score > 0 ? "above" : "below",
        latest_date: recent.last.date,
      }]
    else
      []
    end
  end
end
