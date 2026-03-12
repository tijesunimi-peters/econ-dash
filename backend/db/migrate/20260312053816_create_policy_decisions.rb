class CreatePolicyDecisions < ActiveRecord::Migration[8.1]
  def change
    create_table :policy_decisions do |t|
      t.references :country, null: false, foreign_key: true
      t.string :decision_type, null: false  # interest_rate, qe, regulation, tariff, etc.
      t.date :announcement_date, null: false
      t.date :effective_date, null: false
      t.text :description, null: false
      t.jsonb :impact_sectors, default: []  # Array of affected sectors
      t.integer :expected_lag_months, default: 0  # Months before showing in economic data
      t.string :status, default: 'announced'  # announced, effective, completed, reversed
      t.string :source  # Source of the decision (central bank, govt ministry, etc.)

      t.timestamps
    end

    add_index :policy_decisions, [:country_id, :announcement_date]
    add_index :policy_decisions, [:country_id, :status]
    add_index :policy_decisions, :decision_type
  end
end
