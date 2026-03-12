# Seed structural metrics for Phase 3 implementation
# Covers: population, median_age, labor_participation, life_expectancy, tfp_growth, rd_pct_gdp, education_spending

puts "Seeding structural metrics..."

countries = Country.all.index_by(&:code)
today = Date.today

# Structural metrics data for each country
structural_data = {
  'us' => [
    { metric_type: 'population', value: 340.0, unit: 'millions', source: 'US Census Bureau' },
    { metric_type: 'median_age', value: 38.5, unit: 'years', source: 'US Census Bureau' },
    { metric_type: 'labor_participation', value: 63.0, unit: '%', source: 'US Bureau of Labor Statistics' },
    { metric_type: 'life_expectancy', value: 78.4, unit: 'years', source: 'CDC' },
    { metric_type: 'tfp_growth', value: 1.5, unit: '%', source: 'NBER' },
    { metric_type: 'rd_pct_gdp', value: 3.5, unit: '% of GDP', source: 'NSF' },
    { metric_type: 'education_spending_pct_gdp', value: 6.0, unit: '% of GDP', source: 'OECD Education' }
  ],
  'ca' => [
    { metric_type: 'population', value: 39.7, unit: 'millions', source: 'Statistics Canada' },
    { metric_type: 'median_age', value: 41.5, unit: 'years', source: 'Statistics Canada' },
    { metric_type: 'labor_participation', value: 64.6, unit: '%', source: 'Statistics Canada' },
    { metric_type: 'life_expectancy', value: 82.2, unit: 'years', source: 'Statistics Canada' },
    { metric_type: 'tfp_growth', value: 0.8, unit: '%', source: 'Statistics Canada' },
    { metric_type: 'rd_pct_gdp', value: 1.7, unit: '% of GDP', source: 'Statistics Canada' },
    { metric_type: 'education_spending_pct_gdp', value: 6.2, unit: '% of GDP', source: 'OECD Education' }
  ],
  'jp' => [
    { metric_type: 'population', value: 123.3, unit: 'millions', source: 'Ministry of Internal Affairs' },
    { metric_type: 'median_age', value: 48.7, unit: 'years', source: 'Ministry of Internal Affairs' },
    { metric_type: 'labor_participation', value: 60.1, unit: '%', source: 'Statistics Bureau of Japan' },
    { metric_type: 'life_expectancy', value: 84.5, unit: 'years', source: 'Ministry of Health' },
    { metric_type: 'tfp_growth', value: 0.3, unit: '%', source: 'RIETI' },
    { metric_type: 'rd_pct_gdp', value: 3.6, unit: '% of GDP', source: 'MEXT' },
    { metric_type: 'education_spending_pct_gdp', value: 3.6, unit: '% of GDP', source: 'OECD Education' }
  ],
  'au' => [
    { metric_type: 'population', value: 26.1, unit: 'millions', source: 'ABS' },
    { metric_type: 'median_age', value: 38.5, unit: 'years', source: 'ABS' },
    { metric_type: 'labor_participation', value: 65.2, unit: '%', source: 'ABS' },
    { metric_type: 'life_expectancy', value: 83.1, unit: 'years', source: 'AIHW' },
    { metric_type: 'tfp_growth', value: 0.7, unit: '%', source: 'Department of Industry' },
    { metric_type: 'rd_pct_gdp', value: 2.0, unit: '% of GDP', source: 'DISR' },
    { metric_type: 'education_spending_pct_gdp', value: 6.3, unit: '% of GDP', source: 'OECD Education' }
  ],
  'de' => [
    { metric_type: 'population', value: 83.4, unit: 'millions', source: 'Destatis' },
    { metric_type: 'median_age', value: 48.0, unit: 'years', source: 'Destatis' },
    { metric_type: 'labor_participation', value: 61.5, unit: '%', source: 'Destatis' },
    { metric_type: 'life_expectancy', value: 81.3, unit: 'years', source: 'Destatis' },
    { metric_type: 'tfp_growth', value: 0.5, unit: '%', source: 'DIW Berlin' },
    { metric_type: 'rd_pct_gdp', value: 3.5, unit: '% of GDP', source: 'Destatis' },
    { metric_type: 'education_spending_pct_gdp', value: 6.1, unit: '% of GDP', source: 'OECD Education' }
  ]
}

structural_data.each do |country_code, metrics|
  country = countries[country_code]
  next unless country

  metrics.each do |metric_data|
    metric = country.structural_metrics.find_or_initialize_by(
      metric_type: metric_data[:metric_type],
      date: today
    )

    metric.update!(
      value: metric_data[:value],
      unit: metric_data[:unit],
      source: metric_data[:source]
    )
    puts "✓ Created/Updated: #{country_code.upcase} - #{metric.metric_label}"
  end
end

puts "✅ Structural metrics seeding complete!"
