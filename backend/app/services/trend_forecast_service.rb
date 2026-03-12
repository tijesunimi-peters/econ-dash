class TrendForecastService
  # Forecast future values using simple linear regression
  # Works well for short-term trends (1-2 years)
  #
  # @param historical_data [Array<Hash>] Array of {date: Date, value: Float}
  # @param periods [Integer] Number of periods to forecast
  # @param period_length [Symbol] :month, :quarter, or :year (default :year)
  # @return [Hash] with :forecast (array), :confidence_interval, :r_squared
  def self.forecast_linear(historical_data, periods: 2, period_length: :year)
    return { forecast: [], error: "Insufficient data" } if historical_data.length < 2

    # Extract x (time) and y (value) arrays
    sorted_data = historical_data.sort_by { |d| d[:date] }
    x_values = sorted_data.each_with_index.map { |_, i| i.to_f }
    y_values = sorted_data.map { |d| d[:value].to_f }

    # Calculate linear regression coefficients
    n = x_values.length
    x_mean = x_values.sum / n
    y_mean = y_values.sum / n

    # Slope (m) and intercept (b) for y = mx + b
    numerator = (0...n).sum { |i| (x_values[i] - x_mean) * (y_values[i] - y_mean) }
    denominator = (0...n).sum { |i| (x_values[i] - x_mean) ** 2 }

    return { forecast: [], error: "No variance in data" } if denominator.zero?

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    # Calculate R-squared (goodness of fit)
    y_pred = (0...n).map { |i| slope * x_values[i] + intercept }
    ss_res = (0...n).sum { |i| (y_values[i] - y_pred[i]) ** 2 }
    ss_tot = (0...n).sum { |i| (y_values[i] - y_mean) ** 2 }
    r_squared = 1 - (ss_res / ss_tot)

    # Generate forecast
    last_x = x_values.last
    last_date = sorted_data.last[:date]
    period_increment = case period_length
                       when :month then 1.month
                       when :quarter then 3.months
                       when :year then 1.year
                       else 1.year
                       end

    forecast = (1..periods).map do |i|
      new_x = last_x + i
      predicted_y = slope * new_x + intercept
      predicted_date = last_date + (i * period_increment)

      {
        date: predicted_date,
        value: predicted_y,
        confidence_level: confidence_interval(r_squared, predicted_y, y_values, ss_res, n)
      }
    end

    # Calculate standard error for confidence intervals
    mse = ss_res / (n - 2)  # Mean squared error
    std_error = Math.sqrt(mse)

    {
      forecast: forecast,
      trend: slope.positive? ? "up" : slope.negative? ? "down" : "stable",
      slope: slope.round(6),
      r_squared: r_squared.round(4),
      std_error: std_error.round(4),
      confidence_level: confidence_rating(r_squared)
    }
  end

  # Exponential smoothing for smoother trend lines
  # Alpha parameter (0-1): higher = more responsive to recent changes
  #
  # @param historical_data [Array<Hash>]
  # @param alpha [Float] Smoothing factor (default 0.3)
  # @param periods [Integer] Forecast periods
  # @return [Hash] with smoothed forecast
  def self.forecast_exponential(historical_data, alpha: 0.3, periods: 2)
    return { forecast: [], error: "Insufficient data" } if historical_data.length < 1

    sorted_data = historical_data.sort_by { |d| d[:date] }
    values = sorted_data.map { |d| d[:value].to_f }

    # Initial smoothed value
    smoothed = values.first
    smoothed_values = [smoothed]

    # Exponential smoothing
    (1...values.length).each do |i|
      smoothed = alpha * values[i] + (1 - alpha) * smoothed
      smoothed_values << smoothed
    end

    # Forecast: next value is last smoothed value
    last_date = sorted_data.last[:date]
    forecast = (1..periods).map do |i|
      {
        date: last_date + (i * 1.year),
        value: smoothed_values.last
      }
    end

    {
      forecast: forecast,
      smoothing_factor: alpha,
      note: "Exponential smoothing projects flat trend"
    }
  end

  private

  def self.confidence_interval(r_squared, predicted_y, y_values, ss_res, n)
    # Rough confidence interval: ±std_error * 1.96 for 95% CI
    mse = ss_res / (n - 2)
    std_error = Math.sqrt(mse)
    margin = std_error * 1.96

    {
      lower: predicted_y - margin,
      upper: predicted_y + margin
    }
  end

  def self.confidence_rating(r_squared)
    case r_squared
    when 0.9..1.0 then "Excellent"
    when 0.7...0.9 then "Good"
    when 0.5...0.7 then "Fair"
    when 0.3...0.5 then "Weak"
    else "Very Weak"
    end
  end
end
