# Seed debt metrics for Phase 3 implementation
# Covers: govt_debt_pct_gdp, corp_debt_ratio, hhd_debt_pct_income, deficit_pct_gdp

puts "Seeding debt metrics..."

countries = Country.all.index_by(&:code)
today = Date.today

# Debt metrics data for each country
debt_data = {
  'us' => [
    { metric_type: 'govt_debt_pct_gdp', value: 130.5, trend: 'up', unit: '% of GDP', source: 'US Treasury' },
    { metric_type: 'corp_debt_ratio', value: 2.8, trend: 'stable', unit: 'ratio', source: 'Federal Reserve' },
    { metric_type: 'hhd_debt_pct_income', value: 98.0, trend: 'down', unit: '% of income', source: 'Federal Reserve' },
    { metric_type: 'deficit_pct_gdp', value: 6.2, trend: 'up', unit: '% of GDP', source: 'US Treasury' }
  ],
  'ca' => [
    { metric_type: 'govt_debt_pct_gdp', value: 89.2, trend: 'down', unit: '% of GDP', source: 'Statistics Canada' },
    { metric_type: 'corp_debt_ratio', value: 2.1, trend: 'stable', unit: 'ratio', source: 'Bank of Canada' },
    { metric_type: 'hhd_debt_pct_income', value: 160.5, trend: 'up', unit: '% of income', source: 'Equifax Canada' },
    { metric_type: 'deficit_pct_gdp', value: 1.2, trend: 'down', unit: '% of GDP', source: 'Finance Canada' }
  ],
  'jp' => [
    { metric_type: 'govt_debt_pct_gdp', value: 264.0, trend: 'up', unit: '% of GDP', source: 'Ministry of Finance' },
    { metric_type: 'corp_debt_ratio', value: 1.9, trend: 'down', unit: 'ratio', source: 'Bank of Japan' },
    { metric_type: 'hhd_debt_pct_income', value: 145.0, trend: 'stable', unit: '% of income', source: 'BOJ' },
    { metric_type: 'deficit_pct_gdp', value: 4.5, trend: 'stable', unit: '% of GDP', source: 'Ministry of Finance' }
  ],
  'au' => [
    { metric_type: 'govt_debt_pct_gdp', value: 45.8, trend: 'down', unit: '% of GDP', source: 'AOFM' },
    { metric_type: 'corp_debt_ratio', value: 2.4, trend: 'stable', unit: 'ratio', source: 'RBA' },
    { metric_type: 'hhd_debt_pct_income', value: 155.2, trend: 'up', unit: '% of income', source: 'RBA' },
    { metric_type: 'deficit_pct_gdp', value: 2.1, trend: 'down', unit: '% of GDP', source: 'Australian Treasury' }
  ],
  'de' => [
    { metric_type: 'govt_debt_pct_gdp', value: 60.0, trend: 'down', unit: '% of GDP', source: 'Bundesbank' },
    { metric_type: 'corp_debt_ratio', value: 2.3, trend: 'stable', unit: 'ratio', source: 'ECB' },
    { metric_type: 'hhd_debt_pct_income', value: 91.5, trend: 'stable', unit: '% of income', source: 'Bundesbank' },
    { metric_type: 'deficit_pct_gdp', value: 0.8, trend: 'down', unit: '% of GDP', source: 'German Federal Ministry' }
  ]
}

debt_data.each do |country_code, metrics|
  country = countries[country_code]
  next unless country

  metrics.each do |metric_data|
    metric = country.debt_metrics.find_or_initialize_by(
      metric_type: metric_data[:metric_type],
      date: today
    )

    metric.update!(
      value: metric_data[:value],
      trend: metric_data[:trend],
      unit: metric_data[:unit],
      source: metric_data[:source]
    )
    puts "✓ Created/Updated: #{country_code.upcase} - #{metric.metric_label}"
  end
end

puts "✅ Debt metrics seeding complete!"
