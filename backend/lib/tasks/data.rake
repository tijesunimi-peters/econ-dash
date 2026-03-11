namespace :data do
  desc "Export current database data to db/seed_data.sql"
  task dump: :environment do
    db = ActiveRecord::Base.connection_db_config.configuration_hash
    host = db[:host] || "localhost"
    port = db[:port] || 5432
    database = db[:database]
    username = db[:username] || "econ"

    cmd = "pg_dump -U #{username} -h #{host} -p #{port} --data-only --inserts #{database} > db/seed_data.sql"
    puts "Running: #{cmd}"
    system(cmd)
    puts "Exported to db/seed_data.sql"
  end

  desc "Load data from db/seed_data.sql (no API calls needed)"
  task load: :environment do
    sql_file = Rails.root.join("db/seed_data.sql")
    unless File.exist?(sql_file)
      puts "db/seed_data.sql not found. Run `rails data:dump` first."
      exit 1
    end

    db = ActiveRecord::Base.connection_db_config.configuration_hash
    host = db[:host] || "localhost"
    port = db[:port] || 5432
    database = db[:database]
    username = db[:username] || "econ"

    cmd = "psql -U #{username} -h #{host} -p #{port} -d #{database} -f db/seed_data.sql"
    puts "Running: #{cmd}"
    system(cmd)
    puts "Loaded data from db/seed_data.sql"
  end
end
