import requests
import json


def try_connection(func):
    def attempt_connection(*args, **kwds):
        try:
            func(*args, **kwds)
        except requests.exceptions.ConnectionError as e1:
            print("[Connection Error] Connection canno't be established %s"
                  % str(e1))
        except requests.exceptions.ReadTimeout as e2:
            print("[ConnectionError] Timeout : %s" % str(e2))
    return attempt_connection


"""
Callback functions
"""


def monitor(response, *args, **kwargs):
    header = "From : " + response.url
    content = header
    try:
        body = json.loads(response.text)
        for key, val in body.items():
            content += '\n'
            content += key + "--->" + str(val)
        print(content)
    except json.decoder.JSONDecodeError:
        print(content)
        print("Erreur : Response is not well formatted (JSON Error)")
        print(response.text)


"""
API interactions
"""


@try_connection
def get_status(host, callback=monitor):
    target = '/'.join([host, 'get', 'status'])
    requests.get(target, hooks=dict(response=callback), timeout=10)


@try_connection
def create_collab(host, collab_type, callback=monitor):
    target = '/'.join([host, 'create', collab_type, 'collaborator'])
    requests.post(target, hooks=dict(response=callback), timeout=30)


@try_connection
def start_collab(host, collab_type, callback=monitor):
    target = '/'.join([host, 'start', collab_type, 'collaborator'])
    requests.put(target, hooks=dict(response=callback), timeout=30)


@try_connection
def stopwriting_collab(host, collab_type, callback=monitor):
    target = '/'.join([host, 'stop-writing', collab_type, 'collaborator'])
    requests.put(target, hooks=dict(response=callback), timeout=30)


@try_connection
def stopreading_collab(host, collab_type, callback=monitor):
    target = '/'.join([host, 'stop-reading', collab_type, 'collaborator'])
    requests.put(target, hooks=dict(response=callback), timeout=30)
