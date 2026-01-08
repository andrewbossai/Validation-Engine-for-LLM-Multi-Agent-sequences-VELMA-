import pandas as pd
import json
import requests
from superwise_api.superwise_client import SuperwiseClient
import app_config

QUERY_URL = f'https://api.superwise.ai/v1/query/load'


def query_cubejs(api_url: str, headers: dict, query_params: dict) -> dict:
    response = requests.request("POST", api_url, headers=headers, data=query_params)
    if response.status_code == 200:
        try:
            return response.json()["data"]
        except:
            return
    else:
        print(response.json())
        raise Exception(f"Query failed - HTTP status code: {response.status_code}, response: {response.text}")

def get_app_interactions(internal_dataset_id, filters, fields, sw: SuperwiseClient):
    BEARER_TOKEN = sw.configuration.access_token
    columns = [f"{internal_dataset_id}.{field}" for field in fields]
    query_payload = json.dumps({
        "query": {
            "timezone": "UTC",
            "measures": [],
            "dimensions": columns,
            "filters": filters,
            "limit": 1000
        }
    })

    headers = {
        'x-meta-type': 'dataset',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }

    app_activity = query_cubejs(QUERY_URL, headers, query_payload)

    try:
        app_activity_df = pd.DataFrame(app_activity)

        for column in app_activity_df.columns:
            app_activity_df = app_activity_df.rename(columns = {column: column.split(".")[1]})

        return app_activity_df

    except:
        return None

def use_sql(columns):
    client_id = app_config.client_id
    client_secret = app_config.client_secret
    _sw = SuperwiseClient(client_id=client_id, client_secret=client_secret)

    dataset_name = app_config.swe_dataset
    dataset = _sw.dataset.get(dataset_name)
    internal_dataset_id = dataset.items[0].internal_id

    app_activity_df = get_app_interactions(internal_dataset_id, [], columns, _sw).head()


    return f"\nSQL Output: {app_activity_df}"

# print(use_sql( ["feature_word_count_question"]))

