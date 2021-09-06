import requests


def uploadtoflawcra(filepath):
    with open(filepath, 'rb') as f:
        r = requests.post('https://api.flawcra.cc/cdn/', files={'file': f})
    return r.json()
