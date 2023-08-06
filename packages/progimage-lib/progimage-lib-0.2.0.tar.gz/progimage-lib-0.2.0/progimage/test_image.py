import io
from unittest import TestCase

import requests
from PIL import Image

from progimage.image import upload, rotate, format_type, resize


class ImageTest(TestCase):
    def test_upload(self):
        response = upload(file_url='/Users/chinguyen/workspace/progimage/media/download.jpeg')
        assert response.status_code == 200

    def test_rotate(self):
        image_id = "c99d41e5-8969-42e4-91e0-81a82e801525"
        response = rotate(image_id=image_id, angle=90)
        assert response.status_code == 200

    def test_format_type(self):
        image_id = "c99d41e5-8969-42e4-91e0-81a82e801525"
        response = format_type(image_id=image_id, extension="gif")
        new_image = Image.open(io.BytesIO(response.content))
        assert response.status_code == 200
        assert new_image.format == 'GIF'

    def test_resize(self):
        image_id = "c99d41e5-8969-42e4-91e0-81a82e801525"
        response = resize(image_id=image_id, width=100, height=200)
        new_image = Image.open(io.BytesIO(response.content))
        assert response.status_code == 200
        assert new_image.width == 100
        assert new_image.height == 200
