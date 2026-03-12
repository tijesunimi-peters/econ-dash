class CausalFactorService
  CONFIG_PATH = Rails.root.join("config", "causal_factors.yml")
  ROLLING_WINDOW = 12

  def initialize(country)
    @country = country
    @config = load_config
  end

  def call
    country_code = @country.code.downcase
    country_factors_config = @config.dig(country_code, "sectors") || {}

    return { factors: [], summary: {} } if country_factors_config.empty?

    # Flatten all factors from all sectors
    all_factors = []
    country_factors_config.each do |sector_name, sector_data|
      factors = sector_data.dig("factors") || []
      factors.each do |factor_config|
        all_factors << factor_config.merge("sector_context" => sector_name)
      end
    end

    return { factors: [], summary: {} } if all_factors.empty?

    # Compute data for each factor
    computed_factors = all_factors.map { |f| compute_factor(f) }.compact

    # Rank by correlation strength and recent activity
    ranked_factors = rank_factors(computed_factors)

    # Return top 5
    top_factors = ranked_factors.take(5)

    {
      factors: top_factors,
      summary: {
        total_factors_analyzed: computed_factors.size,
        top_factors_count: top_factors.size,
        highest_correlation: computed_factors.map { |f| f[:correlation_with_sector] }.max&.round(2) || 0,
      }
    }
  end

  private

  def load_config
    @loaded_config ||= YAML.load_file(CONFIG_PATH)
  end

  def compute_factor(factor_config)
    proxy_series_id = factor_config["proxy_series_id"]
    affected_sectors = factor_config["affected_sectors"] || []
    sector_context = factor_config["sector_context"]

    # Get proxy indicator
    proxy_indicator = Indicator.where(source_series_id: proxy_series_id).first
    return nil if proxy_indicator.nil?

    # Get proxy data points
    proxy_data = proxy_indicator.data_points.order(:date).to_a
    return nil if proxy_data.size < ROLLING_WINDOW

    # Detect proxy trend (rising, falling, stable)
    proxy_status, pct_change_3m = detect_proxy_status(proxy_data)

    # Get latest proxy value
    current_proxy_value = proxy_data.last&.value&.to_f

    # Build sector indicators series for correlation
    sector_indicators = get_sector_indicators(affected_sectors)
    return nil if sector_indicators.empty?

    # Compute rolling correlation with each affected sector and take average
    correlation_scores = []
    sector_indicators.each do |sector_name, sector_series|
      next if sector_series.size < ROLLING_WINDOW

      # Align proxy series with sector series by date
      aligned = align_series(proxy_data.map { |p| { date: p.date, value: p.value.to_f } }, sector_series)
      next if aligned[:x].size < ROLLING_WINDOW

      corr = pearson(aligned[:x], aligned[:y])
      correlation_scores << corr
    end

    return nil if correlation_scores.empty?

    avg_correlation = correlation_scores.sum / correlation_scores.size
    confidence = compute_confidence(avg_correlation, proxy_status)

    {
      id: factor_config["id"],
      name: factor_config["name"],
      description: factor_config["description"],
      type: factor_config["type"],
      current_proxy_value: current_proxy_value,
      proxy_status: proxy_status,
      pct_change_3m: pct_change_3m,
      correlation_with_sector: avg_correlation.round(3),
      affected_sectors: affected_sectors,
      sensitivity: factor_config["sensitivity"],
      confidence: confidence,
      rank: 0, # Will be set by rank_factors
    }
  end

  def detect_proxy_status(proxy_data)
    return "unknown", 0.0 if proxy_data.size < 4

    current = proxy_data.last.value.to_f
    prev_month = proxy_data[-2].value.to_f
    three_months_ago = proxy_data[-4].value.to_f

    # 3-month percent change
    if three_months_ago != 0
      pct_change = ((current - three_months_ago) / three_months_ago.abs) * 100
    else
      pct_change = 0
    end

    # Trend detection: compare current to previous
    if current > prev_month * 1.01
      status = "rising"
    elsif current < prev_month * 0.99
      status = "falling"
    else
      status = "stable"
    end

    [status, pct_change]
  end

  def get_sector_indicators(sector_names)
    # Get all sectors matching the names
    sectors = Sector.where(name: sector_names).includes(sub_industries: { indicators: :data_points })
    sector_series = {}

    sectors.each do |sector|
      series = build_sector_series(sector)
      sector_series[sector.name] = series if series.size >= ROLLING_WINDOW
    end

    sector_series
  end

  def build_sector_series(sector)
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

  def compute_confidence(correlation, proxy_status)
    # Confidence is higher if correlation is stronger and proxy is active
    base_confidence = (correlation.abs + 1.0) / 2.0  # Normalize to [0, 1]

    status_multiplier = case proxy_status
                        when "rising", "falling"
                          1.0  # High activity increases confidence
                        when "stable"
                          0.8  # Stable activity reduces confidence slightly
                        else
                          0.5
                        end

    (base_confidence * status_multiplier).round(2)
  end

  def rank_factors(factors)
    # Rank by: correlation strength (high = good), confidence, then by correlation
    factors.sort_by do |f|
      [
        -f[:confidence],          # Higher confidence first (negative = desc)
        -f[:correlation_with_sector].abs,  # Higher correlation (negative = desc)
      ]
    end.each_with_index do |factor, index|
      factor[:rank] = index + 1
    end
  end
end
