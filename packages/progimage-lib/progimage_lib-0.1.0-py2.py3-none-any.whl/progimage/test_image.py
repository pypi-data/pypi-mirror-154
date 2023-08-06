from unittest import TestCase
from progimage.image import upload


class ImageTest(TestCase):
    def test_upload(self):
        response = upload(file_url='/Users/chinguyen/workspace/progimage/media/download.jpeg')
        assert response
