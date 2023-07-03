import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import logging
import json
from datetime import datetime
import pytz

class transform(beam.DoFn):

    def __init__(self):
        self.prefix = str(datetime.now().strftime("%Y%m%d"))
        self.count = 0

    def process(self, data):

        json_data = json.loads(data)

        self.count += 1
        id_track = int(self.prefix + str(self.count).zfill(5))

        utc_time = datetime.strptime(json_data['played_at'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC)
        local_time = utc_time.astimezone(pytz.timezone('Asia/Jakarta'))
        played_at = local_time.strftime("%Y-%m-%d %H:%M:%S")

        album_name = json_data['track']['album']['name']
        album_type = json_data['track']['album']['album_type']
        album_release = str(json_data['track']['album']['release_date'])
        album_link = json_data['track']['album']['external_urls']['spotify']

        asrtists = json_data['track']['artists']
        artist_names = []
        artist_links = []
        for artist in asrtists:
            artist_names.append(artist['name'])
            artist_links.append(artist['external_urls']['spotify'])

        artist_name = ", ".join(artist_names)
        artist_link = ", ".join(artist_links)

        if json_data['context'] == None:

            section_type = "Private playlist"
            section_link = None
            
        else:
    
            section_type = json_data['context']['type']
            section_link = json_data['context']['external_urls']['spotify']

        popularity = int(json_data['track']['popularity'])
        duration = int(json_data['track']['duration_ms'])
        
        res_key = ['id_track', 'played_at', 'album_name', 'album_type', 'album_release_date', 'album_link',
                   'artist_name', 'artist_link', 'section_type', 'section_link', 'popularity', 'duration']
        res_value = [id_track, played_at, album_name, album_type, album_release, album_link, artist_name,
                     artist_link, section_type, section_link, popularity, duration]

        return [dict(zip(res_key, res_value))]


opt = PipelineOptions(
    save_main_session = True,
    runner = 'DataflowRunner',
    temp_location = "gs://arkan-spotify-analytics-resource/temp/",
    job_name = "arkan-spotify-analytics-etl-pipeline",
    project="{YOUR PROJECT ID}",
    template_location = "gs://arkan-spotify-analytics-resource/template/template.json"
)

def pipeline():

    with beam.Pipeline(options=opt) as p:
        (
            p
            |'Extract data from staging area' >> beam.io.ReadFromText("gs://arkan-spotify-analytics-stage-area/")
            |'Transform the data' >> beam.ParDo(transform())
            # |beam.Map(print)
            |'Load into Data Warehouse' >> beam.io.Write(
                beam.io.WriteToBigQuery(
                    project="{YOUR PROJECT ID}",
                    dataset='spotify_analytics',
                    table='denormalized_data',
                    schema=(
                        "id_track:INTEGER,played_at:DATETIME,album_name:STRING,album_type:STRING,\
                        album_release_date:DATE,album_link:STRING,artist_name:STRING,artist_link:STRING,\
                        section_type:STRING,section_link:STRING,popularity:INTEGER,duration:INTEGER"
                    ),
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
                )
            )
        )

if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)
    pipeline()
