import requests
import json
import api_server_info as api


def update_log(query_num, msg):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }

    body = {
        "logId": query_num,
        "response": msg
    }

    params = {
        'apitoken': api.apiToken,
    }

    url = "{}/log/update-response".format(api.url)
    requests.post(url, data=json.dumps(body), params=params, headers=headers)

