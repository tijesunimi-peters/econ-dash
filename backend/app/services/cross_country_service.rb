class CrossCountryService
  def initialize(country, other_country)
    @country = country
    @other = other_country
  end

  def call
    home_sectors = SectorSummaryService.new(@country).call
    other_sectors = SectorSummaryService.new(@other).call

    # Match sectors by name (same 8 sector names in both countries)
    comparisons = home_sectors.map do |hs|
      os = other_sectors.find { |s| s[:name] == hs[:name] }
      next unless os

      home_yoy = hs[:yoy_change_pct] || 0.0
      other_yoy = os[:yoy_change_pct] || 0.0

      {
        sector_name: hs[:name],
        home_country: @country.code,
        other_country: @other.code,
        home_yoy: home_yoy.round(2),
        other_yoy: other_yoy.round(2),
        relative_delta: (home_yoy - other_yoy).round(2),
        home_trend: hs[:trend_direction],
        other_trend: os[:trend_direction],
      }
    end.compact

    {
      home: { id: @country.id, name: @country.name, code: @country.code },
      other: { id: @other.id, name: @other.name, code: @other.code },
      comparisons: comparisons.sort_by { |c| -c[:relative_delta].abs },
    }
  end
end
