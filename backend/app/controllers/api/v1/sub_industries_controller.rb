module Api
  module V1
    class SubIndustriesController < ApplicationController
      def index
        sub_industries = SubIndustry.where(sector_id: params[:sector_id])
        render json: sub_industries.map { |si| sub_industry_json(si) }
      end

      def show
        sub_industry = SubIndustry.includes(indicators: :data_points).find(params[:id])
        render json: sub_industry_json(sub_industry).merge(
          indicators: sub_industry.indicators.map { |i| indicator_summary(i) }
        )
      end

      private

      def sub_industry_json(si)
        {
          id: si.id,
          name: si.name,
          description: si.description,
          sector_id: si.sector_id,
        }
      end

      def indicator_summary(indicator)
        latest = indicator.data_points.order(date: :desc).first
        {
          id: indicator.id,
          name: indicator.name,
          source: indicator.source,
          unit: indicator.unit,
          frequency: indicator.frequency,
          latest_value: latest&.value,
          latest_date: latest&.date,
        }
      end
    end
  end
end
