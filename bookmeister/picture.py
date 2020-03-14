from PIL import Image
import base64
import io


class Picture:
    def __init__(self, path):
        self._image = self.load(path)

    def get(self):
        if self._image:
            return base64.encodebytes(self._image).decode()

    def load(self, path):
        try:
            with open(path, mode='rb') as img:
                image = img.read()
            Image.open(io.BytesIO(image))
            return image
        except (FileNotFoundError, OSError):
            return None

    @staticmethod
    def show(image_data):
        try:
            image = base64.decodebytes(image_data.encode())
            Image.open(io.BytesIO(image)).show()
            return True
        except (FileNotFoundError, OSError, AttributeError):
            return False
