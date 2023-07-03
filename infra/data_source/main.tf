resource "google_cloud_run_service" "spotify_api" {
  name = var.name
  location = var.location

  template {
    spec {
      containers {
        image = var.image
      }
    }
  }
}

data "google_iam_policy" "public_policy" {
  binding { 
    role = var.role
    members = var.members
  }
}

resource "google_cloud_run_service_iam_policy" "spotify_api_policy" {
  location = google_cloud_run_service.spotify_api.location
  project = google_cloud_run_service.spotify_api.project
  service = google_cloud_run_service.spotify_api.name
  policy_data = data.google_iam_policy.public_policy.policy_data
}