class CreateTradeFlowDataPoints < ActiveRecord::Migration[8.1]
  def change
    create_table :trade_flow_data_points do |t|
      t.references :trade_flow, null: false, foreign_key: true
      t.date :date, null: false
      t.decimal :value, null: false, precision: 15, scale: 4
      t.timestamps
    end

    add_index :trade_flow_data_points, [:trade_flow_id, :date], unique: true
    add_index :trade_flow_data_points, :date
  end
end
