class CreateStructuralDataPoints < ActiveRecord::Migration[8.1]
  def change
    create_table :structural_data_points do |t|
      t.references :structural_metric, null: false, foreign_key: true
      t.date :date, null: false
      t.decimal :value, precision: 15, scale: 4, null: false

      t.timestamps
    end

    # Indexes for efficient time-series queries
    add_index :structural_data_points, [:structural_metric_id, :date], unique: true
    add_index :structural_data_points, :date
  end
end
