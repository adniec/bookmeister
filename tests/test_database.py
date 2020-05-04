import pytest

from bookmeister.connection import Database

RECORDS = (
    {
        'Title': 'Test me.',
        'Author': 'Mr Test',
        'Type': 'Test',
        'Publisher': 'Tester',
        'ISBN': 9780340425626,
        'Release': 2020,
        'Language': 'EN',
        'Pages': 999,
        'Quantity': 123,
        'Price': 5.75,
        'Discount': 5,
        'Hardcover': False
    },
    {
        'Title': 'Dancing with tests.',
        'Author': 'Tes Testy',
        'Type': 'Novel',
        'Publisher': 'Tester',
        'ISBN': 9780099578031,
        'Release': 2012,
        'Language': 'NO',
        'Pages': 87,
        'Quantity': 5,
        'Price': 38.27,
        'Discount': 15,
        'Hardcover': False
    },
    {
        'Title': 'Testing madness.',
        'Author': 'Test Tested',
        'Type': 'Criminal',
        'Publisher': 'Tester',
        'ISBN': 9780141190419,
        'Release': 1897,
        'Language': 'ES',
        'Pages': 529,
        'Quantity': 23,
        'Price': 120,
        'Discount': 50,
        'Hardcover': True
    },
    {
        'Title': 'Too fast to test.',
        'Author': 'T. Tested',
        'Type': 'Biography',
        'Publisher': 'Tester',
        'ISBN': 9780515055160,
        'Release': 1972,
        'Language': 'PL',
        'Pages': 728,
        'Quantity': 1,
        'Price': 995,
        'Discount': 0,
        'Hardcover': True
    },
    {
        'Title': 'Testing Illuminati',
        'Author': 'Mysterious Test',
        'Type': 'Thriller',
        'Publisher': 'Tester',
        'ISBN': 9780330102360,
        'Release': 1999,
        'Language': 'IT',
        'Pages': 152,
        'Quantity': 10,
        'Price': 12.99,
        'Discount': 0,
        'Hardcover': True
    },
)


@pytest.fixture(scope='module')
def ids():
    return []


@pytest.mark.live_database
@pytest.mark.dependency
@pytest.mark.run(order=1)
def test_initialization():
    database = Database()
    assert database.url == "https://bookstore-5217.restdb.io/rest/books"


@pytest.mark.live_database
@pytest.mark.dependency(depends=['test_initialization'])
class TestDatabase:

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('record', RECORDS)
    def test_add(self, record):
        assert Database().add(record)

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('query', (
            {'Title': 'Test me.', 'Type': 'Test', 'Quantity': 123},
            {'Title': 'Dancing with tests.'},
            {'Title': 'Testing madness.', 'Type': 'Criminal', 'Release': 1897},
            {'Title': 'Too fast to test.', 'Type': 'Biography', 'Discount': 0},
            {'Type': 'Thriller', 'Pages': 152, 'Quantity': 10, 'Price': 12.99},
    ))
    def test_database_search(self, query, ids):
        result = Database().search(query)
        ids.append(result[0]['_id'])
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

    @pytest.mark.run(order=4)
    def test_database_update(self, ids):
        for number in ids:
            assert Database().update(number, {'Title': 'This is a test.'})

    @pytest.mark.run(order=5)
    def test_database_are_updated(self, ids):
        for number in ids:
            result = Database().search({'_id': number})
            assert result[0]['Title'] == 'This is a test.'

    @pytest.mark.run(order=6)
    def test_database_delete(self, ids):
        for number in ids:
            assert Database().delete(number)

    @pytest.mark.run(order=7)
    def test_database_are_deleted(self, ids):
        for number in ids:
            result = Database().search({'_id': number})
            assert result == []
