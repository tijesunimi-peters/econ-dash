class PercentileService
  FIVE_YEARS_AGO = 5.years

  def initialize(country)
    @country = country
  end

  def call
    indicators = Indicator.joins(sub_industry: { sector: :country })
      .where(sectors: { country_id: @country.id })
      .includes(:data_points, sub_industry: :sector)

    indicators.map { |ind| compute_percentile(ind) }.compact
  end

  private

  def compute_percentile(indicator)
    cutoff = Date.current - FIVE_YEARS_AGO
    points = indicator.data_points.select { |dp| dp.date >= cutoff }.sort_by(&:date)
    return nil if points.size < 10

    values = points.map { |p| p.value.to_f }.sort
    current = points.last.value.to_f
    min_val = values.first
    max_val = values.last

    rank = values.count { |v| v <= current }
    percentile = (rank.to_f / values.size * 100).round(1)

    {
      indicator_id: indicator.id,
      name: indicator.name,
      sector_name: indicator.sub_industry.sector.name,
      sub_industry_name: indicator.sub_industry.name,
      current: current,
      min: min_val,
      max: max_val,
      percentile: percentile,
      classification: classify(percentile),
    }
  end

  def classify(percentile)
    case percentile
    when 0...5 then "extreme_low"
    when 5...20 then "low"
    when 20...80 then "normal"
    when 80...95 then "high"
    else "extreme_high"
    end
  end
end
