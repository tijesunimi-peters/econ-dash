# Solid Queue scheduling for automated data ingestion
#
# Note: In development/test, these are optional.
# In production with Solid Queue running, these will execute automatically.
#
# To manually trigger:
#   docker-compose exec backend bin/rails runner 'IngestStructuralDataJob.perform_now'
#   docker-compose exec backend bin/rails runner 'IngestDebtDataJob.perform_now'

if defined?(Solid)
  Solid::Scheduler.configure do |config|
    # Schedule structural data ingestion daily at 2 AM UTC
    config.recurring(
      "Ingest Structural Data",
      "0 2 * * *",  # Cron: 2 AM every day
      class_name: "IngestStructuralDataJob"
    )

    # Schedule debt data ingestion daily at 2:15 AM UTC (after structural)
    config.recurring(
      "Ingest Debt Data",
      "15 2 * * *",  # Cron: 2:15 AM every day
      class_name: "IngestDebtDataJob"
    )
  end
end
