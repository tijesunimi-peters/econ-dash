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

      def percentiles
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_percentiles/#{country.id}", expires_in: 1.hour) do
          PercentileService.new(country).call
        end
        render json: data
      end

      def anomalies
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_anomalies/#{country.id}", expires_in: 1.hour) do
          AnomalyDetectionService.new(country).call
        end
        render json: data
      end

      def momentum
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_momentum/#{country.id}", expires_in: 1.hour) do
          MomentumScoreboardService.new(country).call
        end
        render json: data
      end

      def business_cycle
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_business_cycle/#{country.id}", expires_in: 1.hour) do
          BusinessCycleService.new(country).call
        end
        render json: data
      end

      def executive_summary
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_executive_summary/#{country.id}", expires_in: 1.hour) do
          ExecutiveSummaryService.new(country).call
        end
        render json: data
      end

      def correlations
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_correlations/#{country.id}", expires_in: 1.hour) do
          CorrelationService.new(country).call
        end
        render json: data
      end

      def compare
        country = Country.find(params[:id])
        other = Country.find(params[:other_id])
        data = Rails.cache.fetch("country_compare/#{country.id}/#{other.id}", expires_in: 1.hour) do
          CrossCountryService.new(country, other).call
        end
        render json: data
      end

      def causal_factors
        country = Country.find(params[:id])
        data = Rails.cache.fetch("country_causal_factors/#{country.id}", expires_in: 1.hour) do
          CausalFactorService.new(country).call
        end
        render json: data
      end

      def by_cycle_phase
        phase = params[:phase]&.downcase
        valid_phases = ["expansion", "peak", "contraction", "trough"]

        return render json: { error: "Invalid phase. Valid phases: #{valid_phases.join(', ')}" }, status: :bad_request unless valid_phases.include?(phase)

        countries_in_phase = Country.all.map do |country|
          cycle_data = Rails.cache.fetch("country_business_cycle/#{country.id}", expires_in: 1.hour) do
            BusinessCycleService.new(country).call
          end

          if cycle_data[:current_phase] == phase
            {
              id: country.id,
              name: country.name,
              code: country.code,
              phase: cycle_data[:current_phase],
              duration_months: cycle_data[:phase_duration_months],
              cycle_position: cycle_data[:cycle_position],
              sector_recommendations: cycle_data[:sector_recommendations]
            }
          end
        end.compact

        render json: { phase: phase, countries: countries_in_phase, count: countries_in_phase.length }
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
