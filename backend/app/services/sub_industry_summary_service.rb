class SubIndustrySummaryService
  def initialize(sector)
    @sector = sector
  end

  def call
    sub_industries = @sector.sub_industries.includes(indicators: :data_points)

    sub_industries.map { |si| build_sub_industry_summary(si) }
  end

  private

  def build_sub_industry_summary(sub_industry)
    indicator_summaries = sub_industry.indicators.map { |ind| build_indicator_summary(ind) }.compact

    avg_yoy = if indicator_summaries.any?
      indicator_summaries.sum { |m| m[:yoy_change_pct] || 0 } / indicator_summaries.size
    else
      0.0
    end

    avg_latest = if indicator_summaries.any?
      indicator_summaries.sum { |m| m[:latest_value] || 0 } / indicator_summaries.size
    else
      0.0
    end

    trend = aggregate_trend(indicator_summaries)

    {
      id: sub_industry.id,
      name: sub_industry.name,
      description: sub_industry.description,
      yoy_change_pct: avg_yoy.round(2),
      trend_direction: trend,
      latest_value_avg: avg_latest.round(2),
      indicators: indicator_summaries,
    }
  end

  def build_indicator_summary(indicator)
    points = indicator.data_points.sort_by(&:date)
    return nil if points.size < 2

    latest = points.last
    yoy_point = find_yoy_point(points, latest.date)

    yoy_change = if yoy_point && yoy_point.value != 0
      ((latest.value - yoy_point.value) / yoy_point.value * 100).to_f
    end

    sparkline = points.last(12).map { |p| p.value.to_f }
    trend = compute_trend(points.last(3))

    {
      id: indicator.id,
      name: indicator.name,
      unit: indicator.unit,
      frequency: indicator.frequency,
      latest_value: latest.value.to_f,
      latest_date: latest.date,
      yoy_change_pct: (yoy_change || 0.0).round(2),
      trend_direction: trend,
      sparkline: sparkline,
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

  def aggregate_trend(summaries)
    return "flat" if summaries.empty?

    ups = summaries.count { |m| m[:trend_direction] == "up" }
    downs = summaries.count { |m| m[:trend_direction] == "down" }

    if ups > downs
      "up"
    elsif downs > ups
      "down"
    else
      "flat"
    end
  end
end
