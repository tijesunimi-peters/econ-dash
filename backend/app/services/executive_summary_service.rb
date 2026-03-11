class ExecutiveSummaryService
  def initialize(country)
    @country = country
  end

  def call
    momentum_data = MomentumScoreboardService.new(@country).call
    anomaly_data = AnomalyDetectionService.new(@country).call
    cycle_data = BusinessCycleService.new(@country).call
    percentile_data = PercentileService.new(@country).call

    {
      traffic_lights: build_traffic_lights(momentum_data),
      narrative: build_narrative(cycle_data, anomaly_data, momentum_data, percentile_data),
      cycle_phase: cycle_data[:current_phase],
      phase_duration: cycle_data[:phase_duration_months],
    }
  end

  private

  def build_traffic_lights(momentum_data)
    momentum_data.map do |sector|
      score = sector[:composite_score]
      accel = sector[:acceleration_direction]

      color = if score > 20 && accel == "accelerating"
        "green"
      elsif score < -20 && accel == "decelerating"
        "red"
      else
        "yellow"
      end

      {
        sector_name: sector[:sector_name],
        color: color,
        score: score,
        direction: accel,
      }
    end
  end

  def build_narrative(cycle_data, anomaly_data, momentum_data, percentile_data)
    bullets = []

    # 1. Cycle phase
    if cycle_data[:current_phase] != "insufficient_data"
      bullets << {
        priority: 1,
        category: "cycle",
        text: "Economy in #{cycle_data[:current_phase]} for #{cycle_data[:phase_duration_months]} months",
      }
    end

    # 2. Critical anomalies
    critical = anomaly_data.select { |a| a[:severity] == "critical" }
    critical.first(3).each do |anomaly|
      bullets << {
        priority: 2,
        category: "anomaly",
        text: "#{anomaly[:indicator_name]} #{anomaly[:z_score].abs}σ #{anomaly[:direction]} rolling mean",
        severity: anomaly[:severity],
      }
    end

    # Warning anomalies
    warnings = anomaly_data.select { |a| a[:severity] == "warning" }
    warnings.first(2).each do |anomaly|
      bullets << {
        priority: 3,
        category: "anomaly",
        text: "#{anomaly[:indicator_name]} #{anomaly[:z_score].abs}σ #{anomaly[:direction]} rolling mean",
        severity: anomaly[:severity],
      }
    end

    # 3. Momentum extremes (top and bottom)
    if momentum_data.any?
      top = momentum_data.first
      if top[:composite_score] > 30
        bullets << {
          priority: 3,
          category: "momentum",
          text: "#{top[:sector_name]} #{top[:acceleration_direction]}, ranked ##{top[:rank]} with score #{top[:composite_score]}",
        }
      end

      bottom = momentum_data.last
      if bottom[:composite_score] < -30
        bullets << {
          priority: 3,
          category: "momentum",
          text: "#{bottom[:sector_name]} #{bottom[:acceleration_direction]}, ranked ##{bottom[:rank]} with score #{bottom[:composite_score]}",
        }
      end
    end

    # 4. Percentile extremes
    extremes = (percentile_data || []).select { |p| p[:classification].in?(["extreme_low", "extreme_high"]) }
    extremes.first(2).each do |pe|
      bullets << {
        priority: 4,
        category: "percentile",
        text: "#{pe[:name]} at #{pe[:percentile].round(0)}th percentile of 5-year range",
      }
    end

    # 5. Leading vs lagging divergence
    if cycle_data[:current_phase] != "insufficient_data"
      leading_up = (cycle_data[:leading_indicators_summary] || []).count { |li| li[:direction] == "accelerating" }
      leading_total = (cycle_data[:leading_indicators_summary] || []).size
      if leading_total > 0
        pct = (leading_up.to_f / leading_total * 100).round(0)
        if pct < 30 || pct > 70
          direction_word = pct > 50 ? "improving" : "deteriorating"
          bullets << {
            priority: 5,
            category: "divergence",
            text: "#{pct}% of leading indicators #{direction_word} — #{leading_up}/#{leading_total} accelerating",
          }
        end
      end
    end

    bullets.sort_by { |b| b[:priority] }
  end
end
