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

jp = Country.find_or_create_by!(code: "JP") { |c| c.name = "Japan" }
au = Country.find_or_create_by!(code: "AU") { |c| c.name = "Australia" }
de = Country.find_or_create_by!(code: "DE") { |c| c.name = "Germany" }

# --- Japan Sectors ---

jp_sectors = {
  "Manufacturing" => {
    description: "Japanese goods production",
    sub_industries: {
      "Overall" => [
        { name: "Industrial Production Index", source: "FRED", source_series_id: "JPNPROINDMISMEI", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Labour" => {
    description: "Japanese employment and workforce",
    sub_industries: {
      "Employment" => [
        { name: "Unemployment Rate", source: "FRED", source_series_id: "LRUNTTTTJPM156S", unit: "Percent", frequency: "monthly" },
        { name: "Employment Level", source: "FRED", source_series_id: "LFEMTTTTJPM647S", unit: "Persons", frequency: "monthly" },
      ],
    },
  },
  "Housing" => {
    description: "Japanese residential real estate",
    sub_industries: {
      "Prices" => [
        { name: "Residential Property Prices", source: "FRED", source_series_id: "QJPN368BIS", unit: "Index 2010=100", frequency: "quarterly" },
      ],
    },
  },
  "Consumer" => {
    description: "Japanese consumer activity",
    sub_industries: {
      "Spending" => [
        { name: "Retail Sales", source: "FRED", source_series_id: "JPNSLRTTO02IXOBM", unit: "Index", frequency: "monthly" },
      ],
      "Confidence" => [
        { name: "Consumer Confidence", source: "FRED", source_series_id: "CSCICP03JPM665S", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Financial" => {
    description: "Japanese banking and interest rates",
    sub_industries: {
      "Interest Rates" => [
        { name: "Call Rate", source: "FRED", source_series_id: "IRSTCI01JPM156N", unit: "Percent", frequency: "monthly" },
        { name: "10-Year Bond Yield", source: "FRED", source_series_id: "IRLTLT01JPM156N", unit: "Percent", frequency: "monthly" },
      ],
    },
  },
  "Inflation" => {
    description: "Japanese price levels",
    sub_industries: {
      "Consumer Prices" => [
        { name: "CPI All Items", source: "FRED", source_series_id: "JPNCPIALLMINMEI", unit: "Index", frequency: "monthly" },
        { name: "Core CPI", source: "FRED", source_series_id: "JPNCPICORMINMEI", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Trade" => {
    description: "Japanese international trade",
    sub_industries: {
      "Trade Balance" => [
        { name: "Exports", source: "FRED", source_series_id: "XTEXVA01JPM667S", unit: "USD", frequency: "monthly" },
        { name: "Imports", source: "FRED", source_series_id: "XTIMVA01JPM667S", unit: "USD", frequency: "monthly" },
      ],
    },
  },
  "Energy" => {
    description: "Japanese energy sector",
    sub_industries: {
      "GDP" => [
        { name: "GDP (energy proxy)", source: "FRED", source_series_id: "NAEXKP01JPQ189S", unit: "Index", frequency: "quarterly" },
      ],
    },
  },
}

jp_sectors.each do |sector_name, sector_data|
  sector = Sector.find_or_create_by!(name: sector_name, country: jp) do |s|
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

# --- Australia Sectors ---

au_sectors = {
  "Manufacturing" => {
    description: "Australian goods production",
    sub_industries: {
      "Overall" => [
        { name: "Industrial Production Index", source: "FRED", source_series_id: "AUSPROINDQISMEI", unit: "Index", frequency: "quarterly" },
      ],
    },
  },
  "Labour" => {
    description: "Australian employment and workforce",
    sub_industries: {
      "Employment" => [
        { name: "Unemployment Rate", source: "FRED", source_series_id: "LRUNTTTTAUM156S", unit: "Percent", frequency: "monthly" },
        { name: "Employment Level", source: "FRED", source_series_id: "LFEMTTTTAUM647S", unit: "Persons", frequency: "monthly" },
      ],
    },
  },
  "Housing" => {
    description: "Australian residential real estate",
    sub_industries: {
      "Prices" => [
        { name: "Residential Property Prices", source: "FRED", source_series_id: "QAUR628BIS", unit: "Index 2010=100", frequency: "quarterly" },
      ],
    },
  },
  "Consumer" => {
    description: "Australian consumer activity",
    sub_industries: {
      "Spending" => [
        { name: "Retail Sales", source: "FRED", source_series_id: "SLRTTO01AUQ659S", unit: "Percent Change", frequency: "quarterly" },
      ],
      "Confidence" => [
        { name: "Consumer Confidence", source: "FRED", source_series_id: "CSCICP03AUM665S", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Financial" => {
    description: "Australian banking and interest rates",
    sub_industries: {
      "Interest Rates" => [
        { name: "Cash Rate", source: "FRED", source_series_id: "IRSTCI01AUM156N", unit: "Percent", frequency: "monthly" },
        { name: "10-Year Bond Yield", source: "FRED", source_series_id: "IRLTLT01AUM156N", unit: "Percent", frequency: "monthly" },
      ],
    },
  },
  "Inflation" => {
    description: "Australian price levels",
    sub_industries: {
      "Consumer Prices" => [
        { name: "CPI All Items", source: "FRED", source_series_id: "AUSCPIALLQINMEI", unit: "Index", frequency: "quarterly" },
        { name: "Core CPI", source: "FRED", source_series_id: "AUSCPICORQINMEI", unit: "Index", frequency: "quarterly" },
      ],
    },
  },
  "Trade" => {
    description: "Australian international trade",
    sub_industries: {
      "Trade Balance" => [
        { name: "Exports", source: "FRED", source_series_id: "XTEXVA01AUM667S", unit: "USD", frequency: "monthly" },
        { name: "Imports", source: "FRED", source_series_id: "XTIMVA01AUM667S", unit: "USD", frequency: "monthly" },
      ],
    },
  },
  "Energy" => {
    description: "Australian energy sector",
    sub_industries: {
      "GDP" => [
        { name: "GDP (energy proxy)", source: "FRED", source_series_id: "NAEXKP01AUQ657S", unit: "AUD", frequency: "quarterly" },
      ],
    },
  },
}

au_sectors.each do |sector_name, sector_data|
  sector = Sector.find_or_create_by!(name: sector_name, country: au) do |s|
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

# --- Germany Sectors ---

de_sectors = {
  "Manufacturing" => {
    description: "German goods production",
    sub_industries: {
      "Overall" => [
        { name: "Industrial Production Index", source: "FRED", source_series_id: "DEUPROINDMISMEI", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Labour" => {
    description: "German employment and workforce",
    sub_industries: {
      "Employment" => [
        { name: "Unemployment Rate", source: "FRED", source_series_id: "LRHUTTTTDEM156S", unit: "Percent", frequency: "monthly" },
        { name: "Employment Level", source: "FRED", source_series_id: "LFEMTTTTDEQ647S", unit: "Persons", frequency: "quarterly" },
      ],
    },
  },
  "Housing" => {
    description: "German residential real estate",
    sub_industries: {
      "Prices" => [
        { name: "Residential Property Prices", source: "FRED", source_series_id: "QDER628BIS", unit: "Index 2010=100", frequency: "quarterly" },
      ],
    },
  },
  "Consumer" => {
    description: "German consumer activity",
    sub_industries: {
      "Spending" => [
        { name: "Retail Sales", source: "FRED", source_series_id: "DEUSLRTTO02IXOBM", unit: "Index", frequency: "monthly" },
      ],
      "Confidence" => [
        { name: "Consumer Confidence", source: "FRED", source_series_id: "CSCICP03DEM665S", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Financial" => {
    description: "German banking and interest rates",
    sub_industries: {
      "Interest Rates" => [
        { name: "3-Month Interbank Rate", source: "FRED", source_series_id: "IR3TIB01DEM156N", unit: "Percent", frequency: "monthly" },
        { name: "10-Year Bund Yield", source: "FRED", source_series_id: "IRLTLT01DEM156N", unit: "Percent", frequency: "monthly" },
      ],
    },
  },
  "Inflation" => {
    description: "German price levels",
    sub_industries: {
      "Consumer Prices" => [
        { name: "CPI All Items", source: "FRED", source_series_id: "DEUCPIALLMINMEI", unit: "Index", frequency: "monthly" },
        { name: "Core CPI", source: "FRED", source_series_id: "DEUCPICORMINMEI", unit: "Index", frequency: "monthly" },
      ],
    },
  },
  "Trade" => {
    description: "German international trade",
    sub_industries: {
      "Trade Balance" => [
        { name: "Exports", source: "FRED", source_series_id: "XTEXVA01DEM667S", unit: "USD", frequency: "monthly" },
        { name: "Imports", source: "FRED", source_series_id: "XTIMVA01DEM667S", unit: "USD", frequency: "monthly" },
      ],
    },
  },
  "Energy" => {
    description: "German energy sector",
    sub_industries: {
      "GDP" => [
        { name: "GDP (energy proxy)", source: "FRED", source_series_id: "NAEXKP01DEQ189S", unit: "Index", frequency: "quarterly" },
      ],
    },
  },
}

de_sectors.each do |sector_name, sector_data|
  sector = Sector.find_or_create_by!(name: sector_name, country: de) do |s|
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

# ── Phase 1 & 2: Policy Timeline and Market Sentiment ──
require_relative 'seeds/policy_decisions'

# ── Phase 3: Structural Metrics and Debt Trends ──
require_relative 'seeds/structural_metrics'
require_relative 'seeds/debt_metrics'

# ── Phase 4: Trade Flows ──
require_relative 'seeds/trade_flows'
