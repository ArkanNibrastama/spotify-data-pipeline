variable "name" {
  default = "spotify-api"
}

variable "location" {
  default = "asia-southeast2"
}

variable "image" {
  default = "{IMAGE CONTAINER PATH IN GCR}"
}

variable "role" {
  default = "roles/run.invoker"
}

variable "members" {
  default = ["allUsers", ]
}
