variable "name" {
  default = "arkan-spotify-analytics-datalake"
}

variable "location" {
  default = "asia-southeast2"
}

variable "storage_class" {
  default = "STANDARD"
}

variable "bucket_level" {
  default = true
}

variable "bucket_access" {
  default = "enforced"
}