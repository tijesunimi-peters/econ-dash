class CreateMarketSentiment < ActiveRecord::Migration[8.1]
  def change
    create_table :market_sentiments do |t|
      t.references :country, null: false, foreign_key: true
      t.string :metric_type, null: false  # cci, pmi, vix, fed_rate_exp, inflation_exp, yield_curve, etc
      t.decimal :value, null: false, precision: 10, scale: 2
      t.date :date, null: false
      t.string :source  # Source of the data
      t.string :trend  # up, down, stable
      t.string :unit  # %, index points, basis points, etc
      t.decimal :prior_value, precision: 10, scale: 2  # Previous value for change calculation
      t.text :notes  # Additional context

      t.timestamps
    end

    add_index :market_sentiments, [:country_id, :metric_type, :date]
    add_index :market_sentiments, [:country_id, :date]
    add_index :market_sentiments, :metric_type
  end
end
