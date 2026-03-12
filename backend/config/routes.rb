Rails.application.routes.draw do
  get "up" => "rails/health#show", as: :rails_health_check

  namespace :api do
    namespace :v1 do
      resources :countries, only: [:index, :show] do
        resources :sectors, only: [:index], shallow: true
        member do
          get :summary
          get :percentiles
          get :anomalies
          get :momentum
          get :business_cycle
          get :executive_summary
          get :correlations
          get :causal_factors
          get :policy_timeline
          get :market_sentiment
          get :structural_trends
          get :debt_trends
          get :structural_forecast
          get 'compare/:other_id', action: :compare
        end
        collection do
          get 'by_cycle_phase/:phase', action: :by_cycle_phase
        end
      end
      resources :sectors, only: [:show] do
        resources :sub_industries, only: [:index], shallow: true
        get :summary, on: :member
      end
      resources :sub_industries, only: [:show] do
        resources :indicators, only: [:index], shallow: true
      end
      resources :indicators, only: [:show] do
        get :series, on: :member
        get :acceleration, on: :member
      end
    end
  end
end
