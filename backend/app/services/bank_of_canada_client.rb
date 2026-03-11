require "net/http"
require "json"

class BankOfCanadaClient
  BASE_URL = "https://www.bankofcanada.ca/valet"

  def fetch_series(series_name, start_date: nil)
    path = "/observations/#{series_name}/json"
    params = {}
    params[:start_date] = start_date.to_s if start_date

    uri = URI("#{BASE_URL}#{path}")
    uri.query = URI.encode_www_form(params) if params.any?

    response = Net::HTTP.get_response(uri)
    raise "Bank of Canada API error: #{response.code}" unless response.is_a?(Net::HTTPSuccess)

    data = JSON.parse(response.body)
    data["observations"].filter_map do |obs|
      value = obs[series_name]&.dig("v")
      next if value.nil? || value == ""

      { date: Date.parse(obs["d"]), value: BigDecimal(value.to_s) }
    end
  end
end
