class CreateSectors < ActiveRecord::Migration[8.1]
  def change
    create_table :sectors do |t|
      t.string :name
      t.references :country, null: false, foreign_key: true
      t.text :description

      t.timestamps
    end
  end
end
