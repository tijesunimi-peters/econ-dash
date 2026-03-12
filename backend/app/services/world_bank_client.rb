require "net/http"
require "json"

class WorldBankClient
  BASE_URL = "https://api.worldbank.org/v2"

  # World Bank indicator codes for key economic metrics
  INDICATORS = {
    population: "SP.POP.TOTL",                    # Total population
    life_expectancy: "SP.DYN.LE00.IN",            # Life expectancy at birth
    labor_participation: "SP.UWT.TLSS.ZS",        # Unemployed (% of total labor force) - inverse
    tfp_growth: "NY.EMP.PRIM.CD",                 # Employment in agriculture
    rd_pct_gdp: "GB.XPD.RSDV.GD.ZS",              # Research & development expenditure (% of GDP)
    education_spending_pct_gdp: "SE.XPD.TOTL.GD.ZS" # Government expenditure on education (% of GDP)
  }.freeze

  # ISO country code mapping
  COUNTRY_CODES = {
    "US" => "USA",
    "CA" => "CAN",
    "JP" => "JPN",
    "AU" => "AUS",
    "DE" => "DEU"
  }.freeze

  def initialize
    # No API key required for World Bank free tier
  end

  def fetch_indicator(indicator_code, country_code, start_year: 2019, end_year: Date.today.year)
    iso_code = COUNTRY_CODES[country_code] || country_code

    uri = URI("#{BASE_URL}/country/#{iso_code}/indicator/#{indicator_code}")
    uri.query = URI.encode_www_form({
      format: "json",
      date: "#{start_year}:#{end_year}",
      per_page: 100
    })

    response = fetch_with_retry(uri)
    parse_response(response)
  rescue => e
    Rails.logger.error("WorldBankClient error fetching #{indicator_code} for #{country_code}: #{e.message}")
    []
  end

  private

  def fetch_with_retry(uri, attempts: 0, max_attempts: 3)
    attempts += 1
    response = Net::HTTP.get_response(uri)

    case response.code.to_i
    when 200..299
      response
    when 500..599
      if attempts < max_attempts
        sleep(2 * attempts)
        fetch_with_retry(uri, attempts: attempts, max_attempts: max_attempts)
      else
        raise "World Bank API error: #{response.code}"
      end
    else
      raise "World Bank API error: #{response.code}"
    end
  end

  def parse_response(response)
    data = JSON.parse(response.body)

    # World Bank returns [metadata, data_array]
    return [] unless data.is_a?(Array) && data.length >= 2

    observations = data[1]
    return [] if observations.nil? || !observations.is_a?(Array)

    observations.filter_map do |obs|
      next unless obs.is_a?(Hash)
      value = obs["value"]
      next if value.nil? || value == ""

      {
        date: Date.new(obs["date"].to_i),
        value: BigDecimal(value.to_s)
      }
    end.sort_by { |o| o[:date] }
  rescue JSON::ParserError => e
    Rails.logger.error("Failed to parse World Bank response: #{e.message}")
    []
  end
end
