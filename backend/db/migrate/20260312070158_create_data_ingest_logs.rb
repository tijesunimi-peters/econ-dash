class CreateDataIngestLogs < ActiveRecord::Migration[8.1]
  def change
    create_table :data_ingest_logs do |t|
      t.string :data_type, null: false # "structural" or "debt"
      t.string :status, null: false    # "success" or "failed"
      t.integer :records_processed     # Count of records updated
      t.text :error_message            # Error details if failed
      t.datetime :completed_at         # When the ingest completed

      t.timestamps
    end

    add_index :data_ingest_logs, [:data_type, :completed_at]
    add_index :data_ingest_logs, :status
  end
end
