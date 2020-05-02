import base64
import pytest

from bookmeister.picture import Picture

IMAGES = ('bookmeister/bookmeister.png',
          'data/bookmeister.ico',
          'data/menu.png',
          'data/notification.png',)


@pytest.fixture
def image_string(path):
    image = Picture(path)
    return image.get()


@pytest.fixture()
def get_bytes(path):
    with open(path, mode='rb') as img:
        return img.read()


@pytest.mark.parametrize('path', IMAGES)
def test_load_existing_image(path, get_bytes):
    tested = Picture.load(path)
    assert tested == get_bytes


@pytest.mark.parametrize('path', IMAGES)
def test_show_existing_image(image_string, mocker):
    mocker.patch('PIL.Image.Image.show')
    assert Picture.show(image_string)


@pytest.mark.parametrize('path', IMAGES)
def test_get_existing_image(image_string, get_bytes):
    assert image_string == base64.encodebytes(get_bytes).decode()


def test_load_not_image(tmpdir):
    path = tmpdir.join('test.txt')
    assert Picture.load(path) is None


def test_load_not_existing_image(tmpdir):
    path = tmpdir / 'image.png'
    assert Picture.load(path) is None


def test_get_not_existing_image(tmpdir):
    path = tmpdir / 'image.png'
    tested = Picture(path)
    assert tested.get() is None


def test_show_corrupted_image(tmpdir):
    image = tmpdir.join('image.png')
    image.write('Test')
    with open(image, mode='rb') as img:
        corrupted = base64.encodebytes(img.read()).decode()
    assert not Picture.show(corrupted)
