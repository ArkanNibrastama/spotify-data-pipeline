from google.cloud import storage

def transfer():

    gcs = storage.Client()

    staging_area = gcs.bucket("arkan-spotify-analytics-stage-area")
    data_lake = gcs.bucket("arkan-spotify-analytics-datalake")

    staging_area_blobs = staging_area.list_blobs()

    for staging_area_blob in staging_area_blobs:

        # get data
        data = staging_area_blob.download_as_text(encoding="utf-8")

        # move data to data lake
        data_lake_blob = data_lake.blob(staging_area_blob.name)
        data_lake_blob.upload_from_string(data, 'application/json')

        # delete data from staging area
        staging_area_blob.delete()