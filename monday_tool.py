import pandas as pd
import requests
import app_config
import ast


monday_apiKey = app_config.monday_apiKey
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : monday_apiKey}

def use_monday(columns_arr):

    query = f"query {{ items_page_by_column_values (board_id: {app_config.monday_table}, columns: [{{column_id: \"task_status\", column_values: [\"Done\"]}}]) {{ items {{ name column_values{{ column{{id title}} value}}}}}}}}"
    data = {'query': query}

    r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
    items = r.json()['data']['items_page_by_column_values']['items']

    index_dict = dict(zip(columns_arr, [-1 for _ in range(len(columns_arr))]))


    for n in range(len(items[0]['column_values'])):
        if items[0]['column_values'][n]['column']['title'] in index_dict:
            index_dict[items[0]['column_values'][n]['column']['title']] = n

    completed_tasks = pd.DataFrame(columns=list(index_dict.keys()))

    for item in items:

        row_values = {}

        for key in index_dict.keys():
            row_values[key] = ast.literal_eval(item['column_values'][index_dict[key]]['value'])

        new_row = pd.DataFrame([row_values])

        completed_tasks = pd.concat([completed_tasks, new_row], ignore_index=True)

    return f"\nMonday Output: {completed_tasks}"

# print(use_monday(["Timeline"]))