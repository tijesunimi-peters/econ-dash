module Api
  module V1
    class CountriesController < ApplicationController
      def index
        countries = Country.all
        render json: countries.map { |c| country_json(c) }
      end

      def show
        country = Country.find(params[:id])
        render json: country_json(country).merge(
          sectors: country.sectors.map { |s| sector_summary(s) }
        )
      end

      def summary
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_summary/#{country.id}", expires_in: 1.hour) do
          SectorSummaryService.new(country).call
        end
        render json: { country: country_json(country), sectors: data }
      end

      private

      def country_json(country)
        { id: country.id, name: country.name, code: country.code }
      end

      def sector_summary(sector)
        { id: sector.id, name: sector.name, description: sector.description }
      end
    end
  end
end
