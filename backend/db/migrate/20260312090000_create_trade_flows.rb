class CreateTradeFlows < ActiveRecord::Migration[8.1]
  def change
    create_table :trade_flows do |t|
      t.references :country, null: false, foreign_key: true
      t.string :flow_type, null: false
      t.decimal :value, null: false, precision: 15, scale: 4
      t.date :date, null: false
      t.string :unit, null: false
      t.string :source
      t.timestamps
    end

    add_index :trade_flows, [:country_id, :flow_type, :date]
    add_index :trade_flows, [:country_id, :date]
    add_index :trade_flows, :flow_type
  end
end
