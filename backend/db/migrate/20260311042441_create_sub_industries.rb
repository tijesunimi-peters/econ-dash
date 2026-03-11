class CreateSubIndustries < ActiveRecord::Migration[8.1]
  def change
    create_table :sub_industries do |t|
      t.string :name
      t.references :sector, null: false, foreign_key: true
      t.text :description

      t.timestamps
    end
  end
end
