Rails.application.routes.draw do
  get "up" => "rails/health#show", as: :rails_health_check

  namespace :api do
    namespace :v1 do
      resources :countries, only: [:index, :show] do
        resources :sectors, only: [:index], shallow: true
      end
      resources :sectors, only: [:show] do
        resources :sub_industries, only: [:index], shallow: true
      end
      resources :sub_industries, only: [:show] do
        resources :indicators, only: [:index], shallow: true
      end
      resources :indicators, only: [:show] do
        get :series, on: :member
      end
    end
  end
end
