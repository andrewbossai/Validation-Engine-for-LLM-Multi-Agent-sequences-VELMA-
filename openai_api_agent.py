import requests
from superwise_api.superwise_client import SuperwiseClient
import app_config

app_name = app_config.app_name
client_id = app_config.client_id
client_secret = app_config.client_secret

sw = SuperwiseClient(client_id=client_id, client_secret=client_secret)
app_id = app_config.app_id
app_token = app_config.app_token
def call_model(prompt):
    endpoint_url = f"https://api.superwise.ai/v1/app-worker/{app_id}/v1/ask"

    payload = {
        "chat_history": [],
        "input": prompt,
        "prompt": ""
    }

    headers = {
        "x-api-token": app_token
    }

    resp = requests.post(endpoint_url, json=payload, headers=headers)
    app_response = resp.json()

    return app_response["output"]