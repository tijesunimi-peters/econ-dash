class CreateDebtMetrics < ActiveRecord::Migration[8.1]
  def change
    create_table :debt_metrics do |t|
      t.references :country, null: false, foreign_key: true
      t.string :metric_type, null: false
      t.decimal :value, null: false, precision: 10, scale: 2
      t.date :date, null: false
      t.string :unit, null: false
      t.string :trend
      t.string :source
      t.timestamps
    end

    add_index :debt_metrics, [:country_id, :metric_type, :date]
    add_index :debt_metrics, [:country_id, :date]
    add_index :debt_metrics, :metric_type
  end
end
