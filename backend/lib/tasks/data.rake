namespace :data do
  desc "Export current database data to db/seed_data.sql"
  task dump: :environment do
    config = ActiveRecord::Base.connection_db_config.configuration_hash
    env = pg_env(config)

    cmd = "pg_dump --data-only --inserts #{config[:database]} > db/seed_data.sql"
    puts "Running: #{cmd}"
    system(env, cmd)
    puts "Exported to db/seed_data.sql"
  end

  desc "Load data from db/seed_data.sql (no API calls needed)"
  task load: :environment do
    sql_file = Rails.root.join("db/seed_data.sql")
    unless File.exist?(sql_file)
      puts "db/seed_data.sql not found. Run `rails data:dump` first."
      exit 1
    end

    config = ActiveRecord::Base.connection_db_config.configuration_hash
    env = pg_env(config)

    cmd = "psql -d #{config[:database]} -f db/seed_data.sql"
    puts "Running: #{cmd}"
    system(env, cmd)
    puts "Loaded data from db/seed_data.sql"
  end

  def pg_env(config)
    env = {}
    env["PGHOST"] = config[:host] if config[:host]
    env["PGPORT"] = config[:port].to_s if config[:port]
    env["PGUSER"] = config[:username] if config[:username]
    env["PGPASSWORD"] = config[:password] if config[:password]
    env
  end
end
