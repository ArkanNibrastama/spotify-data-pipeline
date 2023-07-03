variable "project_id" {
  default = "{YOUR PROJECT ID}"
}

variable "file_name" {
  default = "transfer_func.zip"
}

variable "bucket" {
  default = "arkan-spotify-analytics-resource"
}

variable "file_source" {
  default = "../etl_pipeline/transfer_func/transfer_func.zip"
}

variable "func_name" {
  default = "transfer-function"
}

variable "location" {
  default = "asia-southeast2"
}
variable "desc" {
  default = "transfer data from staging area into data lake"
}

variable "runtime" {
  default = "python310"
}

variable "entry_point" {
  default = "transfer_data"
}

variable "role" {
  default = "roles/run.invoker"
}

variable "members" {
  default = [
    "allUsers"
  ]
}

variable "max_instance_count" {
  default = 1
}

variable "memory" {
  default = "256M"
}
variable "timeout" {
  default = 60
}
