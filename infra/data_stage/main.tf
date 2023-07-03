resource "google_storage_bucket" "staging_area" {
    project = var.project_id
    name = var.name
    location = var.location
    storage_class = var.storage_class
    uniform_bucket_level_access = var.bucket_level
    public_access_prevention = var.bucket_access
}