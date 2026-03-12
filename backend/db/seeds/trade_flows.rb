# Seed trade flow metrics for Phase 4 implementation
# Covers: exports, imports, FDI, supply chain metrics

puts "Seeding trade flow metrics..."

countries = Country.all.index_by { |c| c.code.downcase }
today = Date.today

# Trade flow data for each country
# Based on World Bank data and realistic estimates
trade_data = {
  'us' => [
    { flow_type: 'exports_pct_gdp', value: 12.5, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'imports_pct_gdp', value: 15.2, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'trade_balance_pct_gdp', value: -2.7, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'fdi_inflows_pct_gdp', value: 2.1, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'supply_chain_concentration', value: 28, unit: 'index', source: 'Seed Data' },
    { flow_type: 'export_diversification', value: 0.72, unit: 'index', source: 'Seed Data' },
    { flow_type: 'import_dependency_ratio', value: 1.2, unit: 'ratio', source: 'Seed Data' }
  ],
  'ca' => [
    { flow_type: 'exports_pct_gdp', value: 32.1, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'imports_pct_gdp', value: 34.5, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'trade_balance_pct_gdp', value: -2.4, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'fdi_inflows_pct_gdp', value: 2.8, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'supply_chain_concentration', value: 35, unit: 'index', source: 'Seed Data' },
    { flow_type: 'export_diversification', value: 0.65, unit: 'index', source: 'Seed Data' },
    { flow_type: 'import_dependency_ratio', value: 1.3, unit: 'ratio', source: 'Seed Data' }
  ],
  'jp' => [
    { flow_type: 'exports_pct_gdp', value: 18.4, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'imports_pct_gdp', value: 17.9, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'trade_balance_pct_gdp', value: 0.5, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'fdi_inflows_pct_gdp', value: 0.8, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'supply_chain_concentration', value: 22, unit: 'index', source: 'Seed Data' },
    { flow_type: 'export_diversification', value: 0.78, unit: 'index', source: 'Seed Data' },
    { flow_type: 'import_dependency_ratio', value: 0.97, unit: 'ratio', source: 'Seed Data' }
  ],
  'au' => [
    { flow_type: 'exports_pct_gdp', value: 22.3, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'imports_pct_gdp', value: 19.8, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'trade_balance_pct_gdp', value: 2.5, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'fdi_inflows_pct_gdp', value: 1.5, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'supply_chain_concentration', value: 38, unit: 'index', source: 'Seed Data' },
    { flow_type: 'export_diversification', value: 0.58, unit: 'index', source: 'Seed Data' },
    { flow_type: 'import_dependency_ratio', value: 0.89, unit: 'ratio', source: 'Seed Data' }
  ],
  'de' => [
    { flow_type: 'exports_pct_gdp', value: 45.6, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'imports_pct_gdp', value: 39.2, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'trade_balance_pct_gdp', value: 6.4, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'fdi_inflows_pct_gdp', value: 1.2, unit: '% of GDP', source: 'World Bank' },
    { flow_type: 'supply_chain_concentration', value: 25, unit: 'index', source: 'Seed Data' },
    { flow_type: 'export_diversification', value: 0.81, unit: 'index', source: 'Seed Data' },
    { flow_type: 'import_dependency_ratio', value: 0.86, unit: 'ratio', source: 'Seed Data' }
  ]
}

trade_data.each do |country_code, flows|
  country = countries[country_code]
  next unless country

  flows.each do |flow_data|
    flow = country.trade_flows.find_or_initialize_by(
      flow_type: flow_data[:flow_type],
      date: today
    )

    flow.update!(
      value: flow_data[:value],
      unit: flow_data[:unit],
      source: flow_data[:source]
    )
    puts "✓ Created/Updated: #{country_code.upcase} - #{flow.metric_label}"
  end
end

puts "✅ Trade flow metrics seeding complete!"
