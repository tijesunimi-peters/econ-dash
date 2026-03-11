require "net/http"
require "json"

class StatcanClient
  BASE_URL = "https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadTbl/en"
  VECTOR_URL = "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action"

  # StatCan Web Data Service
  WDS_URL = "https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadTbl/en"

  def fetch_vector(vector_id, start_date: nil)
    uri = URI("https://www150.statcan.gc.ca/t1/tbl1/en/tv.action")
    params = { Vid: vector_id }
    uri.query = URI.encode_www_form(params)

    response = Net::HTTP.get_response(uri)
    raise "StatCan API error: #{response.code}" unless response.is_a?(Net::HTTPSuccess)

    # Parse the response - StatCan returns CSV or JSON depending on endpoint
    parse_statcan_response(response.body, start_date)
  end

  private

  def parse_statcan_response(body, start_date)
    data = JSON.parse(body)
    observations = data["object"]&.dig("vectorDataPoint") || []

    observations.filter_map do |obs|
      date = Date.parse(obs["refPer"])
      next if start_date && date < start_date

      { date: date, value: BigDecimal(obs["value"].to_s) }
    end
  rescue JSON::ParserError
    Rails.logger.error("Failed to parse StatCan response")
    []
  end
end
