from PIL import Image
import base64
import io


def open_image(path):
    try:
        with open(path, mode='rb') as img:
            image = img.read()
        Image.open(io.BytesIO(image))
        return image
    except (FileNotFoundError, OSError):
        return None


def show(image_data):
    try:
        image = base64.decodebytes(image_data.encode())
        Image.open(io.BytesIO(image)).show()
        return True
    except (FileNotFoundError, OSError, AttributeError):
        return False


def get_image(path):
    image = open_image(path)
    if image:
        return base64.encodebytes(image).decode()
