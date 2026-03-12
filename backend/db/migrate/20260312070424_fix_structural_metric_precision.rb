class FixStructuralMetricPrecision < ActiveRecord::Migration[8.1]
  def change
    # Increase precision for large values (e.g., population in millions)
    change_column :structural_metrics, :value, :decimal, precision: 15, scale: 4
    change_column :structural_data_points, :value, :decimal, precision: 15, scale: 4
  end
end
