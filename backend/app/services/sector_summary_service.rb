class SectorSummaryService
  def initialize(country)
    @country = country
  end

  def call
    sectors = @country.sectors.includes(sub_industries: { indicators: :data_points })

    sectors.map { |sector| build_sector_summary(sector) }
  end

  private

  def build_sector_summary(sector)
    indicator_metrics = sector.indicators.map { |ind| compute_indicator_metrics(ind) }.compact

    avg_yoy = if indicator_metrics.any?
      indicator_metrics.sum { |m| m[:yoy_change_pct] || 0 } / indicator_metrics.size
    else
      0.0
    end

    trend = aggregate_trend(indicator_metrics)

    {
      id: sector.id,
      name: sector.name,
      description: sector.description,
      yoy_change_pct: avg_yoy.round(2),
      trend_direction: trend,
      indicator_count: indicator_metrics.size,
    }
  end

  def compute_indicator_metrics(indicator)
    points = indicator.data_points.sort_by(&:date)
    return nil if points.size < 2

    latest = points.last
    previous = points[-2]

    yoy_point = find_yoy_point(points, latest.date)

    yoy_change = if yoy_point && yoy_point.value != 0
      ((latest.value - yoy_point.value) / yoy_point.value * 100).to_f
    end

    trend = compute_trend(points.last(3))

    {
      yoy_change_pct: yoy_change || 0.0,
      trend_direction: trend,
    }
  end

  def find_yoy_point(points, reference_date)
    target = reference_date - 1.year
    points.min_by { |p| (p.date - target).abs }
      .then { |p| (p.date - target).abs <= 45 ? p : nil }
  end

  def compute_trend(recent_points)
    return "flat" if recent_points.size < 3

    values = recent_points.map { |p| p.value.to_f }
    if values[0] < values[1] && values[1] < values[2]
      "up"
    elsif values[0] > values[1] && values[1] > values[2]
      "down"
    else
      "flat"
    end
  end

  def aggregate_trend(metrics)
    return "flat" if metrics.empty?

    ups = metrics.count { |m| m[:trend_direction] == "up" }
    downs = metrics.count { |m| m[:trend_direction] == "down" }

    if ups > downs
      "up"
    elsif downs > ups
      "down"
    else
      "flat"
    end
  end
end
