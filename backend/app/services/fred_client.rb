require "net/http"
require "json"

class FredClient
  BASE_URL = "https://api.stlouisfed.org/fred"

  def initialize(api_key = ENV.fetch("FRED_API_KEY"))
    @api_key = api_key
  end

  def fetch_series(series_id, start_date: nil)
    params = {
      series_id: series_id,
      api_key: @api_key,
      file_type: "json",
    }
    params[:observation_start] = start_date.to_s if start_date

    uri = URI("#{BASE_URL}/series/observations")
    uri.query = URI.encode_www_form(params)

    response = Net::HTTP.get_response(uri)
    raise "FRED API error: #{response.code}" unless response.is_a?(Net::HTTPSuccess)

    JSON.parse(response.body)["observations"].filter_map do |obs|
      next if obs["value"] == "."

      { date: Date.parse(obs["date"]), value: BigDecimal(obs["value"]) }
    end
  end
end
