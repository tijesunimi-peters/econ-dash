class CorrelationService
  ROLLING_WINDOW = 12
  DIVERGENCE_THRESHOLD = 0.4

  def initialize(country)
    @country = country
  end

  def call
    sectors = @country.sectors.includes(sub_industries: { indicators: :data_points })

    # Build sector-level aggregated monthly series
    sector_series = {}
    sectors.each do |sector|
      series = build_sector_series(sector)
      sector_series[sector.name] = series if series.size >= 12
    end

    sector_names = sector_series.keys.sort
    return { matrix: [], labels: [], divergences: [] } if sector_names.size < 2

    # Compute pairwise correlations
    matrix = []
    divergences = []

    sector_names.each do |row_name|
      row = []
      sector_names.each do |col_name|
        if row_name == col_name
          row << 1.0
        else
          aligned = align_series(sector_series[row_name], sector_series[col_name])
          if aligned[:x].size >= 6
            full_corr = pearson(aligned[:x], aligned[:y])
            row << full_corr.round(3)

            # Rolling correlation for divergence detection
            if aligned[:x].size >= ROLLING_WINDOW
              recent_x = aligned[:x].last(ROLLING_WINDOW)
              recent_y = aligned[:y].last(ROLLING_WINDOW)
              rolling_corr = pearson(recent_x, recent_y)
              gap = (full_corr - rolling_corr).abs
              if gap >= DIVERGENCE_THRESHOLD
                divergences << {
                  sector_a: row_name,
                  sector_b: col_name,
                  full_period_correlation: full_corr.round(3),
                  rolling_correlation: rolling_corr.round(3),
                  gap: gap.round(3),
                }
              end
            end
          else
            row << nil
          end
        end
      end
      matrix << row
    end

    # Deduplicate divergences (A-B and B-A are the same)
    unique_divergences = divergences.uniq { |d| [d[:sector_a], d[:sector_b]].sort }

    {
      labels: sector_names,
      matrix: matrix,
      divergences: unique_divergences.sort_by { |d| -d[:gap] },
    }
  end

  private

  def build_sector_series(sector)
    # Average all indicator values per month for this sector
    monthly = Hash.new { |h, k| h[k] = [] }

    sector.indicators.each do |ind|
      ind.data_points.each do |dp|
        month_key = dp.date.beginning_of_month
        monthly[month_key] << dp.value.to_f
      end
    end

    monthly.sort_by { |date, _| date }.map do |date, values|
      { date: date, value: values.sum / values.size }
    end
  end

  def align_series(series_a, series_b)
    dates_b = series_b.each_with_object({}) { |p, h| h[p[:date]] = p[:value] }

    x = []
    y = []
    series_a.each do |point|
      if dates_b.key?(point[:date])
        x << point[:value]
        y << dates_b[point[:date]]
      end
    end

    { x: x, y: y }
  end

  def pearson(x, y)
    n = x.size
    return 0.0 if n < 2

    mean_x = x.sum / n
    mean_y = y.sum / n

    cov = x.zip(y).sum { |xi, yi| (xi - mean_x) * (yi - mean_y) }
    std_x = Math.sqrt(x.sum { |xi| (xi - mean_x)**2 })
    std_y = Math.sqrt(y.sum { |yi| (yi - mean_y)**2 })

    return 0.0 if std_x == 0 || std_y == 0

    cov / (std_x * std_y)
  end
end
