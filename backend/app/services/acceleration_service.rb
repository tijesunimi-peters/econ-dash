class AccelerationService
  STABLE_THRESHOLD = 0.5 # percentage points

  def initialize(indicator)
    @indicator = indicator
  end

  def call
    points = @indicator.data_points.order(:date).to_a
    return empty_result if points.size < 7 # need at least 7 points for two 3-month windows

    latest_values = points.last(7).map { |p| { date: p.date, value: p.value.to_f } }

    current_window = latest_values.last(3)
    prior_window = latest_values[0, 3]

    rate_of_change = compute_rate_of_change(current_window.first[:value], current_window.last[:value])
    prior_rate = compute_rate_of_change(prior_window.first[:value], prior_window.last[:value])
    acceleration = rate_of_change - prior_rate

    direction = if acceleration > STABLE_THRESHOLD
      "accelerating"
    elsif acceleration < -STABLE_THRESHOLD
      "decelerating"
    else
      "stable"
    end

    {
      indicator_id: @indicator.id,
      indicator_name: @indicator.name,
      rate_of_change: rate_of_change.round(4),
      acceleration: acceleration.round(4),
      direction: direction,
      current_value: points.last.value.to_f,
      computed_at: Time.current.iso8601,
    }
  end

  private

  def compute_rate_of_change(start_val, end_val)
    return 0.0 if start_val == 0
    ((end_val - start_val) / start_val.abs) * 100
  end

  def empty_result
    {
      indicator_id: @indicator.id,
      indicator_name: @indicator.name,
      rate_of_change: nil,
      acceleration: nil,
      direction: "insufficient_data",
      current_value: nil,
      computed_at: Time.current.iso8601,
    }
  end
end
