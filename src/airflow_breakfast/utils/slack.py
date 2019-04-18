import json

import requests
from airflow.hooks.base_hook import BaseHook


def send_slack_message(text):
    connection = BaseHook.get_connection("slack")
    headers = {"Content-type": "application/json"}
    requests.post(connection.host, data=json.dumps({"text": text}), headers=headers)

# Setup:
# https://api.slack.com/incoming-webhooks
# create app
# create webhook url, point to slack channel
# store host in airflow connection
