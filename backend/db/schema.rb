# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.1].define(version: 2026_03_11_042443) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "pg_catalog.plpgsql"

  create_table "countries", force: :cascade do |t|
    t.string "code"
    t.datetime "created_at", null: false
    t.string "name"
    t.datetime "updated_at", null: false
    t.index ["code"], name: "index_countries_on_code"
  end

  create_table "data_points", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.date "date"
    t.bigint "indicator_id", null: false
    t.datetime "updated_at", null: false
    t.decimal "value"
    t.index ["indicator_id", "date"], name: "index_data_points_on_indicator_id_and_date", unique: true
    t.index ["indicator_id"], name: "index_data_points_on_indicator_id"
  end

  create_table "indicators", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.string "frequency"
    t.string "name"
    t.string "source"
    t.string "source_series_id"
    t.bigint "sub_industry_id", null: false
    t.string "unit"
    t.datetime "updated_at", null: false
    t.index ["sub_industry_id"], name: "index_indicators_on_sub_industry_id"
  end

  create_table "sectors", force: :cascade do |t|
    t.bigint "country_id", null: false
    t.datetime "created_at", null: false
    t.text "description"
    t.string "name"
    t.datetime "updated_at", null: false
    t.index ["country_id"], name: "index_sectors_on_country_id"
  end

  create_table "sub_industries", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.text "description"
    t.string "name"
    t.bigint "sector_id", null: false
    t.datetime "updated_at", null: false
    t.index ["sector_id"], name: "index_sub_industries_on_sector_id"
  end

  add_foreign_key "data_points", "indicators"
  add_foreign_key "indicators", "sub_industries"
  add_foreign_key "sectors", "countries"
  add_foreign_key "sub_industries", "sectors"
end
