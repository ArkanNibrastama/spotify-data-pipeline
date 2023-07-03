resource "google_bigquery_dataset" "data_warehouse" {
  dataset_id = var.dataset_id
  location = var.location
}

resource "google_bigquery_table" "tracks_table" {
  dataset_id = google_bigquery_dataset.data_warehouse.dataset_id
  table_id = var.table_id
  schema = var.schema
  deletion_protection = false
}