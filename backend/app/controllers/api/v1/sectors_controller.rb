module Api
  module V1
    class SectorsController < ApplicationController
      def index
        sectors = Sector.where(country_id: params[:country_id])
        render json: sectors.map { |s| sector_json(s) }
      end

      def show
        sector = Sector.find(params[:id])
        render json: sector_json(sector).merge(
          sub_industries: sector.sub_industries.map { |si| sub_industry_summary(si) }
        )
      end

      private

      def sector_json(sector)
        {
          id: sector.id,
          name: sector.name,
          description: sector.description,
          country_id: sector.country_id,
        }
      end

      def sub_industry_summary(si)
        { id: si.id, name: si.name, description: si.description }
      end
    end
  end
end
