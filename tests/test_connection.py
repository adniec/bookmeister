from json import loads
import pytest
from requests.exceptions import ConnectionError

from bookmeister.connection import Database


@pytest.fixture(params=(
        ('add', ({'Publisher': 'Tester'},)),
        ('update', ('5eb00ffce332cd260015d67c', {'Publisher': 'Tester'})),
        ('delete', ('5eb00ffce332cd260015d67c',)),
))
def database(value, request, mocker):
    mocked = mocker.patch('requests.request')
    mocked.return_value.text = value
    return getattr(Database(), request.param[0])(*request.param[1])


def test_initialization():
    database = Database()
    assert isinstance(database.url, str)
    assert isinstance(database.headers, dict)


@pytest.mark.parametrize('value,expected', (
        ('[{"_id": "5eb00ffce332cd260015d67c"}]', True),
        ('', False),
        ('[]', False),
        ('Response 500', False),
))
def test_database_action(value, expected, database):
    assert database == expected


@pytest.mark.parametrize('value', (
        '[{"_id": "5eb00ffce332cd260015d67c"}]',
        '[{"Title": "Test me."}, {"Title": "Test me 2."}]',
        '[]',
))
def test_database_search(value, mocker):
    mocked = mocker.patch('requests.request')
    mocked.return_value.text = value
    assert Database().search({'Publisher': 'Tester'}) == loads(value)


@pytest.mark.parametrize('method,args', (
        ('add', ({'Publisher': 'Tester'},)),
        ('search', ({'Title': 'Test me.', 'Type': 'Test'},)),
        ('update', ('5eb00ffce332cd260015d67c', {'Type': 'Tested'})),
        ('delete', ('5eb00ffce332cd260015d67c',)),
))
def test_no_connection(method, args, mocker):
    mocked = mocker.patch('requests.request')
    mocked.side_effect = ConnectionError
    assert not getattr(Database(), method)(*args)


@pytest.mark.parametrize('message,result', (
        ('{"msg":"OK","uploadid":"b7ddaa0ed","ids":["5fc00c0d"]}', '5fc00c0d'),
        ('{"msg":"OK","uploadid":"a2fg99mg8","ids":["j8ar24im"]}', 'j8ar24im'),
        ('[]', None)
))
def test_database_upload_image(message, result, mocker):
    mocker.patch('builtins.open')
    mocked = mocker.patch('requests.request')
    mocked.return_value.text = message
    assert Database().upload_image('/home/user') == result

