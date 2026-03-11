Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins ENV.fetch("DASH_ORIGIN", "http://localhost:8050")

    resource "*",
      headers: :any,
      methods: [:get]
  end
end
