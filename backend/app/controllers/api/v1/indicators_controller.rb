module Api
  module V1
    class IndicatorsController < ApplicationController
      def index
        indicators = Indicator.where(sub_industry_id: params[:sub_industry_id])
        render json: indicators.map { |i| indicator_json(i) }
      end

      def show
        indicator = Indicator.find(params[:id])
        render json: indicator_json(indicator)
      end

      def series
        indicator = Indicator.find(params[:id])
        points = indicator.data_points.order(:date)

        if params[:start_date].present?
          points = points.where("date >= ?", params[:start_date])
        end
        if params[:end_date].present?
          points = points.where("date <= ?", params[:end_date])
        end

        render json: {
          indicator: indicator_json(indicator),
          data: points.map { |dp| { date: dp.date, value: dp.value } },
        }
      end

      private

      def indicator_json(indicator)
        {
          id: indicator.id,
          name: indicator.name,
          source: indicator.source,
          source_series_id: indicator.source_series_id,
          unit: indicator.unit,
          frequency: indicator.frequency,
          sub_industry_id: indicator.sub_industry_id,
        }
      end
    end
  end
end
