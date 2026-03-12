# Seed initial policy decisions for Phase 1 implementation
# Run with: docker-compose exec backend bin/rails db:seed:policy_decisions

puts "Seeding policy decisions..."

countries = Country.all.index_by(&:code)

# US Federal Reserve Policies
[
  {
    country_code: 'us',
    decision_type: 'interest_rate',
    announcement_date: '2026-03-12',
    effective_date: '2026-03-15',
    description: 'Federal Reserve raises federal funds rate 25bps to 5.50%',
    impact_sectors: ['Financial', 'Consumer', 'Real Estate'],
    expected_lag_months: 1,
    status: 'effective',
    source: 'FOMC Statement'
  },
  {
    country_code: 'us',
    decision_type: 'interest_rate',
    announcement_date: '2026-01-28',
    effective_date: '2026-02-01',
    description: 'Federal Reserve holds rates steady at 5.25%',
    impact_sectors: [],
    expected_lag_months: 0,
    status: 'effective',
    source: 'FOMC Statement'
  },
  {
    country_code: 'us',
    decision_type: 'qe',
    announcement_date: '2024-12-18',
    effective_date: '2025-01-01',
    description: 'Fed begins Quantitative Tightening (QT) pause, holding balance sheet steady',
    impact_sectors: ['Financial', 'Consumer'],
    expected_lag_months: 2,
    status: 'effective',
    source: 'FOMC Statement'
  },
  {
    country_code: 'us',
    decision_type: 'tariff',
    announcement_date: '2026-02-15',
    effective_date: '2026-03-01',
    description: 'Administration imposes 15% tariff on semiconductors from TSMC',
    impact_sectors: ['Manufacturing', 'Technology', 'Consumer'],
    expected_lag_months: 1,
    status: 'effective',
    source: 'USTR Announcement'
  },
].each do |policy_data|
  country = countries[policy_data.delete(:country_code)]
  next unless country

  policy = country.policy_decisions.find_or_initialize_by(
    decision_type: policy_data[:decision_type],
    announcement_date: Date.parse(policy_data[:announcement_date])
  )

  policy.update!(
    effective_date: Date.parse(policy_data[:effective_date]),
    description: policy_data[:description],
    impact_sectors: policy_data[:impact_sectors],
    expected_lag_months: policy_data[:expected_lag_months],
    status: policy_data[:status],
    source: policy_data[:source]
  )
  puts "✓ Created/Updated: #{policy.description}"
end

# Canada Bank of Canada Policies
[
  {
    country_code: 'ca',
    decision_type: 'interest_rate',
    announcement_date: '2026-03-04',
    effective_date: '2026-03-04',
    description: 'Bank of Canada cuts policy rate 25bps to 4.25%',
    impact_sectors: ['Financial', 'Consumer', 'Real Estate'],
    expected_lag_months: 1,
    status: 'effective',
    source: 'BOC Rate Decision'
  },
  {
    country_code: 'ca',
    decision_type: 'interest_rate',
    announcement_date: '2026-01-22',
    effective_date: '2026-01-22',
    description: 'Bank of Canada cuts policy rate 50bps to 4.50%',
    impact_sectors: ['Financial', 'Consumer'],
    expected_lag_months: 1,
    status: 'effective',
    source: 'BOC Rate Decision'
  },
].each do |policy_data|
  country = countries[policy_data.delete(:country_code)]
  next unless country

  policy = country.policy_decisions.find_or_initialize_by(
    decision_type: policy_data[:decision_type],
    announcement_date: Date.parse(policy_data[:announcement_date])
  )

  policy.update!(
    effective_date: Date.parse(policy_data[:effective_date]),
    description: policy_data[:description],
    impact_sectors: policy_data[:impact_sectors],
    expected_lag_months: policy_data[:expected_lag_months],
    status: policy_data[:status],
    source: policy_data[:source]
  )
  puts "✓ Created/Updated: #{policy.description}"
end

# Japan Bank of Japan Policies
[
  {
    country_code: 'jp',
    decision_type: 'interest_rate',
    announcement_date: '2026-03-19',
    effective_date: '2026-03-19',
    description: 'Bank of Japan raises policy rate to 0.50%, first hike in 17 years',
    impact_sectors: ['Financial', 'Export Competitiveness'],
    expected_lag_months: 2,
    status: 'effective',
    source: 'BOJ Monetary Policy Decision'
  },
  {
    country_code: 'jp',
    decision_type: 'qe',
    announcement_date: '2024-07-31',
    effective_date: '2024-08-05',
    description: 'Bank of Japan begins scaling back YCC (Yield Curve Control)',
    impact_sectors: ['Financial', 'JGBs'],
    expected_lag_months: 3,
    status: 'completed',
    source: 'BOJ Announcement'
  },
].each do |policy_data|
  country = countries[policy_data.delete(:country_code)]
  next unless country

  policy = country.policy_decisions.find_or_initialize_by(
    decision_type: policy_data[:decision_type],
    announcement_date: Date.parse(policy_data[:announcement_date])
  )

  policy.update!(
    effective_date: Date.parse(policy_data[:effective_date]),
    description: policy_data[:description],
    impact_sectors: policy_data[:impact_sectors],
    expected_lag_months: policy_data[:expected_lag_months],
    status: policy_data[:status],
    source: policy_data[:source]
  )
  puts "✓ Created/Updated: #{policy.description}"
end

# Australia Reserve Bank of Australia Policies
[
  {
    country_code: 'au',
    decision_type: 'interest_rate',
    announcement_date: '2026-02-03',
    effective_date: '2026-02-03',
    description: 'RBA holds cash rate steady at 4.35%',
    impact_sectors: [],
    expected_lag_months: 0,
    status: 'effective',
    source: 'RBA Rate Decision'
  },
  {
    country_code: 'au',
    decision_type: 'regulation',
    announcement_date: '2026-01-15',
    effective_date: '2026-02-01',
    description: 'ASIC tightens lending standards for property investment',
    impact_sectors: ['Real Estate', 'Financial'],
    expected_lag_months: 1,
    status: 'effective',
    source: 'ASIC Regulatory Update'
  },
].each do |policy_data|
  country = countries[policy_data.delete(:country_code)]
  next unless country

  policy = country.policy_decisions.find_or_initialize_by(
    decision_type: policy_data[:decision_type],
    announcement_date: Date.parse(policy_data[:announcement_date])
  )

  policy.update!(
    effective_date: Date.parse(policy_data[:effective_date]),
    description: policy_data[:description],
    impact_sectors: policy_data[:impact_sectors],
    expected_lag_months: policy_data[:expected_lag_months],
    status: policy_data[:status],
    source: policy_data[:source]
  )
  puts "✓ Created/Updated: #{policy.description}"
end

# Germany European Central Bank Policies
[
  {
    country_code: 'de',
    decision_type: 'interest_rate',
    announcement_date: '2026-03-12',
    effective_date: '2026-03-18',
    description: 'ECB holds main refinancing rate at 4.50%',
    impact_sectors: [],
    expected_lag_months: 0,
    status: 'effective',
    source: 'ECB Governing Council Decision'
  },
  {
    country_code: 'de',
    decision_type: 'regulation',
    announcement_date: '2026-02-01',
    effective_date: '2026-03-01',
    description: 'EU Green Taxonomy strengthens ESG requirements for financial institutions',
    impact_sectors: ['Financial', 'Energy', 'Manufacturing'],
    expected_lag_months: 2,
    status: 'effective',
    source: 'EU Commission Directive'
  },
].each do |policy_data|
  country = countries[policy_data.delete(:country_code)]
  next unless country

  policy = country.policy_decisions.find_or_initialize_by(
    decision_type: policy_data[:decision_type],
    announcement_date: Date.parse(policy_data[:announcement_date])
  )

  policy.update!(
    effective_date: Date.parse(policy_data[:effective_date]),
    description: policy_data[:description],
    impact_sectors: policy_data[:impact_sectors],
    expected_lag_months: policy_data[:expected_lag_months],
    status: policy_data[:status],
    source: policy_data[:source]
  )
  puts "✓ Created/Updated: #{policy.description}"
end

puts "✅ Policy decision seeding complete!"
