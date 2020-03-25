import requests

from utils.config import get_config


def invoke_get_request(endpoint, params={}):
    config = get_config()

    url = f"http://{config['rest']['server']}:{config['rest']['port']}{endpoint}"
    payload = requests.get(url=url, params=params)

    return payload.json()


def get_chart_url(name):
    config = get_config()
    return f"http://{config['rest']['server']}:{config['rest']['port']}/chart/{name}"