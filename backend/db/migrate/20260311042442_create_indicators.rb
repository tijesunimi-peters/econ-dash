class CreateIndicators < ActiveRecord::Migration[8.1]
  def change
    create_table :indicators do |t|
      t.string :name
      t.references :sub_industry, null: false, foreign_key: true
      t.string :source
      t.string :source_series_id
      t.string :unit
      t.string :frequency

      t.timestamps
    end
  end
end
