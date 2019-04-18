import json
import pathlib
import posixpath

import airflow
import requests
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from airflow_breakfast.utils.slack import send_slack_message

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(10)}

dag = DAG(
    dag_id="2_rockets",
    default_args=args,
    description="DAG downloading rocket launches from Launch Library.",  # e.g. https://launchlibrary.net/1.4/launch?startdate=2019-04-10&enddate=2019-04-21
    schedule_interval="0 0 * * *",
)


def _download_rocket_launches(ds, next_ds, **_):
    query = f"https://launchlibrary.net/1.4/launch?startdate={ds}&enddate={next_ds}"
    result_path = f"/data/rocket_launches/ds={ds}"
    pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)
    result_file = posixpath.join(result_path, "launches.json")

    response = requests.get(query)
    with open(result_file, "w") as f:
        f.write(response.text)
        print(f"Wrote result to file {result_file}")


download_rocket_launches = PythonOperator(
    task_id="download_rocket_launches",
    python_callable=_download_rocket_launches,
    provide_context=True,
    dag=dag,
)


def _print_stats(ds, **_):
    with open(f"/data/rocket_launches/ds={ds}/launches.json") as f:
        data = json.load(f)

        for launch in data["launches"]:
            print(f"Rocket launched today: {launch['name']}")
            if launch["vidURLs"]:
                for vidurl in launch["vidURLs"]:
                    print(f"Watch the video here: {vidurl}")


print_stats = PythonOperator(
    task_id="print_stats", python_callable=_print_stats, provide_context=True, dag=dag
)

download_rocket_launches >> print_stats


def _slack_message(ds, **_):
    with open(f"/data/rocket_launches/ds={ds}/launches.json") as f:
        data = json.load(f)

        for launch in data["launches"]:
            message = f"🚀 Rocket launched today ({ds}): {launch['name']}\n"
            if launch["vidURLs"]:
                for vidurl in launch["vidURLs"]:
                    message += f"Watch the video here: {vidurl}\n"

            send_slack_message(message)


slack_message = PythonOperator(
    task_id="slack_message",
    python_callable=_slack_message,
    provide_context=True,
    dag=dag,
)

download_rocket_launches >> slack_message
