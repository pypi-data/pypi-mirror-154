import requests

URL = "http://127.0.0.1:8000/images/"


def upload(file_url: str):
    files = {"image": open(file_url, 'rb')}
    response = requests.post(URL, files=files)
    return response


def rotate(image_id: str, angle=int):
    url = f"{URL}{image_id}/display/?rotate={angle}"
    response = requests.get(url)
    return response


def format_type(image_id: str, extension=str):
    url = f"{URL}{image_id}/display/?extension={extension}"
    response = requests.get(url)
    return response


def resize(image_id: str, width, height):
    url = f"{URL}{image_id}/display/?width={width}&height={height}"
    response = requests.get(url)
    return response
