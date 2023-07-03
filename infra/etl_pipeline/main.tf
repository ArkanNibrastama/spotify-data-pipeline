# composer
resource "google_service_account" "composer_service_acc" {
  account_id = "composer"
  display_name = "composer"
}

resource "google_project_iam_member" "editor_iam" {
  project = var.project_id
  member = "serviceAccount:${google_service_account.composer_service_acc.email}"
  role = "roles/editor"
}

resource "google_project_iam_member" "composer_admin_iam" {
  project = var.project_id
  member = "serviceAccount:${google_service_account.composer_service_acc.email}"
  role = "roles/composer.admin"
}

resource "google_composer_environment" "composer_env" {
  name   = "arkan-spotify-analytics-env"
  region = "asia-southeast1"
 config {
    software_config {
      image_version = "composer-1.20.12-airflow-2.4.3"
    }
    node_config {
      service_account = google_service_account.composer_service_acc.email
    }
  }
}

# transfer function
resource "google_storage_bucket_object" "transfer_function_file"{

    name   = var.file_name
    bucket = var.bucket
    source = var.file_source

}

resource "google_cloudfunctions2_function" "transfer_function" {
  name = var.func_name
  location = var.location
  description = var.desc

  build_config {
    runtime = var.runtime
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = google_storage_bucket_object.transfer_function_file.bucket
        object = google_storage_bucket_object.transfer_function_file.name
      }
    }
  }

  service_config {
    max_instance_count  = var.max_instance_count
    available_memory    = var.memory
    timeout_seconds     = var.timeout
  }
}


resource "google_cloud_run_service_iam_binding" "default" {
  location = google_cloudfunctions2_function.transfer_function.location
  service = google_cloudfunctions2_function.transfer_function.name

  role   = var.role
  members = var.members
}