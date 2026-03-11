class CreateDataPoints < ActiveRecord::Migration[8.1]
  def change
    create_table :data_points do |t|
      t.references :indicator, null: false, foreign_key: true
      t.date :date
      t.decimal :value

      t.timestamps
    end
    add_index :data_points, [:indicator_id, :date], unique: true
  end
end
