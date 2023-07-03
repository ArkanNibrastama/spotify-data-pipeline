variable "dataset_id" {
  default = "spotify_analytics"
}

variable "location" {
  default = "asia-southeast2"
}

variable "table_id" {
  default = "denormalized_data"
}

variable "schema" {
  default = <<EOF
  [
    {
      "name" : "id_track",
      "type" : "INTEGER",
      "mode" : "NULLABLE",
      "description" : "unique value for each tracks."
    },
    {
      "name" : "played_at",
      "type" : "DATETIME",
      "mode" : "NULLABLE",
      "description" : "time when the track is played."
    },
    {
      "name" : "album_name",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description" : "name of album."
    },
    {
      "name" : "album_type",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description" : "type of an album."
    },
    {
      "name" : "album_release_date",
      "type" : "DATE",
      "mode" : "NULLABLE",
      "description" : "albums release date."
    },
    {
      "name" : "album_link",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description" : "spotify link for the album."
    },
    {
      "name" : "artist_name",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description" : "artist's name of the album."
    },
    {
      "name" : "artist_link",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description" : "spotify link for the artist."
    },
    {
      "name" : "section_type",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description" : "from what section the track is played."
    },
    {
      "name" : "section_link",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description" : "spotify link for the section."
    },
    {
      "name" : "popularity",
      "type" : "INTEGER",
      "mode" : "NULLABLE",
      "description" : "popularity of the track (0 - 100) with 100 is the most popular track."
    },
    {
      "name" : "duration",
      "type" : "INTEGER",
      "mode" : "NULLABLE",
      "description" : "The track length in milliseconds."
    }
  ]
  EOF
}