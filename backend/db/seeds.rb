# US and Canada with sectors, sub-industries, and real data source series IDs

us = Country.find_or_create_by!(code: "US") { |c| c.name = "United States" }
ca = Country.find_or_create_by!(code: "CA") { |c| c.name = "Canada" }

# --- US Sectors ---

us_sectors = {
  "Manufacturing" => {
    description: "Goods production including durable and non-durable manufacturing",
    sub_industries: {
      "Overall Manufacturing" => [
        { name: "Industrial Production Index", source: "FRED", source_series_id: "INDPRO", unit: "Index 2017=100", frequency: "monthly" },
        { name: "ISM Manufacturing PMI", source: "FRED", source_series_id: "MANEMP", unit: "Thousands", frequency: "monthly" },
        { name: "Manufacturing GDP Contribution", source: "FRED", source_series_id: "VAPGDPMA", unit: "Billions USD", frequency: "quarterly" },
      ],
      "Durable Goods" => [
        { name: "Durable Goods Orders", source: "FRED", source_series_id: "DGORDER", unit: "Millions USD", frequency: "monthly" },
      ],
      "Non-Durable Goods" => [
        { name: "Non-Durable Goods Orders", source: "FRED", source_series_id: "ANDENO", unit: "Millions USD", frequency: "monthly" },
      ],
    },
  },
  "Labour" => {
    description: "Employment, wages, and workforce participation",
    sub_industries: {
      "Employment" => [
        { name: "Unemployment Rate", source: "FRED", source_series_id: "UNRATE", unit: "Percent", frequency: "monthly" },
        { name: "Nonfarm Payrolls", source: "FRED", source_series_id: "PAYEMS", unit: "Thousands", frequency: "monthly" },
        { name: "Initial Jobless Claims", source: "FRED", source_series_id: "ICSA", unit: "Number", frequency: "weekly" },
      ],
      "Wages" => [
        { name: "Average Hourly Earnings", source: "FRED", source_series_id: "CES0500000003", unit: "USD", frequency: "monthly" },
      ],
      "Participation" => [
        { name: "Labor Force Participation Rate", source: "FRED", source_series_id: "CIVPART", unit: "Percent", frequency: "monthly" },
      ],
    },
  },
  "Housing" => {
    description: "Residential real estate and construction",
    sub_industries: {
      "Construction" => [
        { name: "Housing Starts", source: "FRED", source_series_id: "HOUST", unit: "Thousands", frequency: "monthly" },
        { name: "Building Permits", source: "FRED", source_series_id: "PERMIT", unit: "Thousands", frequency: "monthly" },
      ],
      "Sales" => [
        { name: "Existing Home Sales", source: "FRED", source_series_id: "EXHOSLUSM495S", unit: "Number", frequency: "monthly" },
        { name: "New Home Sales", source: "FRED", source_series_id: "HSN1F", unit: "Thousands", frequency: "monthly" },
      ],
      "Prices" => [
        { name: "Case-Shiller Home Price Index", source: "FRED", source_series_id: "CSUSHPINSA", unit: "Index Jan 2000=100", frequency: "monthly" },
      ],
    },
  },
  "Consumer" => {
    description: "Consumer spending, confidence, and retail activity",
    sub_industries: {
      "Spending" => [
        { name: "Retail Sales", source: "FRED", source_series_id: "RSAFS", unit: "Millions USD", frequency: "monthly" },
        { name: "Personal Consumption Expenditures", source: "FRED", source_series_id: "PCE", unit: "Billions USD", frequency: "monthly" },
      ],
      "Confidence" => [
        { name: "Consumer Sentiment (U of M)", source: "FRED", source_series_id: "UMCSENT", unit: "Index 1966=100", frequency: "monthly" },
      ],
      "Credit" => [
        { name: "Consumer Credit Outstanding", source: "FRED", source_series_id: "TOTALSL", unit: "Billions USD", frequency: "monthly" },
      ],
    },
  },
  "Financial" => {
    description: "Banking, interest rates, and financial markets",
    sub_industries: {
      "Interest Rates" => [
        { name: "Federal Funds Rate", source: "FRED", source_series_id: "FEDFUNDS", unit: "Percent", frequency: "monthly" },
        { name: "10-Year Treasury Yield", source: "FRED", source_series_id: "GS10", unit: "Percent", frequency: "monthly" },
        { name: "2-Year Treasury Yield", source: "FRED", source_series_id: "GS2", unit: "Percent", frequency: "monthly" },
      ],
      "Credit Spreads" => [
        { name: "BAA Corporate Bond Spread", source: "FRED", source_series_id: "BAA10Y", unit: "Percent", frequency: "monthly" },
      ],
      "Money Supply" => [
        { name: "M2 Money Supply", source: "FRED", source_series_id: "M2SL", unit: "Billions USD", frequency: "monthly" },
      ],
    },
  },
  "Energy" => {
    description: "Oil, gas, and energy production",
    sub_industries: {
      "Oil" => [
        { name: "WTI Crude Oil Price", source: "FRED", source_series_id: "DCOILWTICO", unit: "USD/Barrel", frequency: "daily" },
      ],
      "Natural Gas" => [
        { name: "Henry Hub Natural Gas Price", source: "FRED", source_series_id: "DHHNGSP", unit: "USD/MMBtu", frequency: "daily" },
      ],
    },
  },
  "Inflation" => {
    description: "Price levels and purchasing power",
    sub_industries: {
      "Consumer Prices" => [
        { name: "CPI All Items", source: "FRED", source_series_id: "CPIAUCSL", unit: "Index 1982-84=100", frequency: "monthly" },
        { name: "Core CPI (ex Food & Energy)", source: "FRED", source_series_id: "CPILFESL", unit: "Index 1982-84=100", frequency: "monthly" },
      ],
      "Producer Prices" => [
        { name: "PPI All Commodities", source: "FRED", source_series_id: "PPIACO", unit: "Index 1982=100", frequency: "monthly" },
      ],
      "PCE Inflation" => [
        { name: "PCE Price Index", source: "FRED", source_series_id: "PCEPI", unit: "Index 2017=100", frequency: "monthly" },
        { name: "Core PCE Price Index", source: "FRED", source_series_id: "PCEPILFE", unit: "Index 2017=100", frequency: "monthly" },
      ],
    },
  },
  "Trade" => {
    description: "International trade and balance of payments",
    sub_industries: {
      "Trade Balance" => [
        { name: "Trade Balance", source: "FRED", source_series_id: "BOPGSTB", unit: "Millions USD", frequency: "monthly" },
        { name: "Exports", source: "FRED", source_series_id: "BOPGEXP", unit: "Millions USD", frequency: "monthly" },
        { name: "Imports", source: "FRED", source_series_id: "BOPGIMP", unit: "Millions USD", frequency: "monthly" },
      ],
    },
  },
}

us_sectors.each do |sector_name, sector_data|
  sector = Sector.find_or_create_by!(name: sector_name, country: us) do |s|
    s.description = sector_data[:description]
  end

  sector_data[:sub_industries].each do |si_name, indicators|
    sub_industry = SubIndustry.find_or_create_by!(name: si_name, sector: sector)

    indicators.each do |ind|
      Indicator.find_or_create_by!(source_series_id: ind[:source_series_id]) do |i|
        i.name = ind[:name]
        i.sub_industry = sub_industry
        i.source = ind[:source]
        i.unit = ind[:unit]
        i.frequency = ind[:frequency]
      end
    end
  end
end

# --- Canada Sectors ---

ca_sectors = {
  "Manufacturing" => {
    description: "Canadian goods production",
    sub_industries: {
      "Overall Manufacturing" => [
        { name: "Manufacturing Sales", source: "FRED", source_series_id: "CANRGDPMANQISMEI", unit: "Index", frequency: "quarterly" },
      ],
    },
  },
  "Labour" => {
    description: "Canadian employment and workforce",
    sub_industries: {
      "Employment" => [
        { name: "Unemployment Rate", source: "FRED", source_series_id: "LRUNTTTTCAM156S", unit: "Percent", frequency: "monthly" },
        { name: "Employment Level", source: "FRED", source_series_id: "LFEMTTTTCAM647S", unit: "Persons", frequency: "monthly" },
      ],
      "Participation" => [
        { name: "Labour Force Participation", source: "FRED", source_series_id: "LRAC25TTCAM156S", unit: "Percent", frequency: "monthly" },
      ],
    },
  },
  "Housing" => {
    description: "Canadian residential real estate",
    sub_industries: {
      "Construction" => [
        { name: "Housing Starts", source: "FRED", source_series_id: "CANHOUST", unit: "Units", frequency: "monthly" },
      ],
      "Prices" => [
        { name: "House Price Index", source: "FRED", source_series_id: "QCAR628BIS", unit: "Index 2010=100", frequency: "quarterly" },
      ],
    },
  },
  "Consumer" => {
    description: "Canadian consumer activity",
    sub_industries: {
      "Spending" => [
        { name: "Retail Sales", source: "FRED", source_series_id: "CARSLM", unit: "CAD", frequency: "monthly" },
      ],
      "Confidence" => [
        { name: "Consumer Confidence", source: "FRED", source_series_id: "CSCICP03CAM665S", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Financial" => {
    description: "Canadian banking and interest rates",
    sub_industries: {
      "Interest Rates" => [
        { name: "Bank of Canada Overnight Rate", source: "BankOfCanada", source_series_id: "V39079", unit: "Percent", frequency: "daily" },
        { name: "Canada 10-Year Bond Yield", source: "FRED", source_series_id: "IRLTLT01CAM156N", unit: "Percent", frequency: "monthly" },
      ],
    },
  },
  "Energy" => {
    description: "Canadian energy sector",
    sub_industries: {
      "Oil" => [
        { name: "Canada GDP Oil & Gas", source: "FRED", source_series_id: "CANRGDPMINQISMEI", unit: "Index", frequency: "quarterly" },
      ],
    },
  },
  "Inflation" => {
    description: "Canadian price levels",
    sub_industries: {
      "Consumer Prices" => [
        { name: "CPI All Items", source: "FRED", source_series_id: "CPALCY01CAM661N", unit: "Percent Change", frequency: "monthly" },
        { name: "Core CPI", source: "FRED", source_series_id: "CPGRLE01CAM659N", unit: "Percent Change", frequency: "monthly" },
      ],
    },
  },
  "Trade" => {
    description: "Canadian international trade",
    sub_industries: {
      "Trade Balance" => [
        { name: "Trade Balance", source: "FRED", source_series_id: "XTIMVA01CAM667S", unit: "CAD", frequency: "monthly" },
      ],
    },
  },
}

ca_sectors.each do |sector_name, sector_data|
  sector = Sector.find_or_create_by!(name: sector_name, country: ca) do |s|
    s.description = sector_data[:description]
  end

  sector_data[:sub_industries].each do |si_name, indicators|
    sub_industry = SubIndustry.find_or_create_by!(name: si_name, sector: sector)

    indicators.each do |ind|
      Indicator.find_or_create_by!(source_series_id: ind[:source_series_id]) do |i|
        i.name = ind[:name]
        i.sub_industry = sub_industry
        i.source = ind[:source]
        i.unit = ind[:unit]
        i.frequency = ind[:frequency]
      end
    end
  end
end

puts "Seeded #{Country.count} countries, #{Sector.count} sectors, #{SubIndustry.count} sub-industries, #{Indicator.count} indicators"
