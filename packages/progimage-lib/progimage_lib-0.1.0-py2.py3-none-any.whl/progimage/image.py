import requests

URL = "http://127.0.0.1:8000/images/"


def upload(file_url):
    files = {"image": open(file_url, 'rb')}
    response = requests.post(URL, files=files)
    return response
