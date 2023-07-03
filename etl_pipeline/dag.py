import airflow
from airflow import models
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import timedelta

args = {

    'owner' : 'Arkan',
    # 'start_date' : days_ago(1),
    'retries' : 1,
    'retry_delay' : timedelta(seconds=60),
    'dataflow_default_options': {

        "project": "{YOUR PEOJECT ID}",
        "location": "asia-southeast2",
        "zone": "asia-southeast2-a",
        "tempLocation": "gs://arkan-spotify-analytics-resource/temp"

    }

}

with models.DAG(

    dag_id="spotify_analytics",
    default_args=args,
    schedule_interval=timedelta(days=7),
    start_date=days_ago(1)

) as dag:
    
    etl_job = DataflowTemplatedJobStartOperator(
        task_id = "etl_pipeline",
        job_name="arkan-spotify-analytics-etl-pipeline",
        location="asia-southeast2",
        template="gs://arkan-spotify-analytics-resource/template/template.json"
    )

    transfer_data = SimpleHttpOperator(
        task_id = "transfer_data",
        method='GET',
        http_conn_id='http_default',
        endpoint='transfer-function'

    )

    etl_job >> transfer_data
