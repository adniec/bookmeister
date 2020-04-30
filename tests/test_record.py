import pytest

from bookmeister import record


@pytest.fixture(name='raised')
def is_value_error_raised(request, args):
    try:
        test_name = request.node.function.__name__
        {'test_length_check': record.check_length,
         'test_number_check': record.check_number,
         'test_isbn_check': record.check_isbn,
         'test_lang_check': record.check_lang_code,
         'test_price_check': record.check_price,
         }[test_name](*args)
        return True
    except ValueError:
        return False


def test_fields():
    assert record.FIELDS == ('Title', 'Author', 'Type', 'Publisher', 'ISBN',
                             'Release', 'Language', 'Pages', 'Quantity',
                             'Price', 'Discount')


@pytest.mark.parametrize(('args', 'expected'), (
        (['Test this short sentence.'], True),
        (('Test' * 10, 0, 100), True),
        (('Test', 1, 4), True),
        (('Test me.', 8, 10), True),
        (('', 0, 100), True),
        (['Test'], True),
        (('AB', 2, 2), True),
        (('ABC', 2, 2), False),
        (('Test', 0, 3), False),
        (('', 1, 100), False),
        ([''], False),
        (['Test' * 30], False),
))
def test_length_check(raised, expected):
    assert raised == expected


@pytest.mark.parametrize(('args', 'expected'), (
        (['12'], True),
        (['0123'], True),
        (('1958', 1800, 2020), True),
        (('1800', 1800, 2020), True),
        (('2020', 1800, 2020), True),
        (('-12', 0, 100), False),
        (['-12'], False),
        (['456.789'], False),
        (['1.23'], False),
        (['1234567890'], False),
))
def test_number_check(raised, expected):
    assert raised == expected


@pytest.mark.parametrize(('args', 'expected'), (
        (['9780330102360'], True),
        (['9781856132657'], True),
        (['9780141028279'], True),
        (['9780099578031'], True),
        (['9780141190419'], True),
        (['9780515055160'], True),
        (['9780340425626'], True),
        (['TestTestTestT'], False),
        (['9780test25626'], False),
        (['97803404256AB'], False),
        (['1234567890123'], False),
        (['0123012301230'], False),
        (['781856132657'], False),
        (['1413304540'], False),
        (['1932982118'], False),
        (['01010101101'], False),
        (['test'], False),
        ([''], False),
))
def test_isbn_check(raised, expected):
    assert raised == expected


@pytest.mark.parametrize(('args', 'expected'), (
        (['EN'], True),
        (['PL'], True),
        (['ES'], True),
        (['SK'], True),
        (['E2'], False),
        (['23'], False),
        (['+-'], False),
        (['T/'], False),
        (['T*'], False),
        (['T~'], False),
        (['Test'], False),
        (['T'], False),
))
def test_lang_check(raised, expected):
    assert raised == expected


@pytest.mark.parametrize(('args', 'expected'), (
        (['1234'], True),
        (['12.34'], True),
        (['9999'], True),
        (['0'], True),
        (['100000'], False),
        (['-123'], False),
        (['-1'], False),
        (['12.345'], False),
        (['12,34'], False),
        (['123Test'], False),
        (['Test'], False),
        ([''], False),
))
def test_price_check(raised, expected):
    assert raised == expected


def test_empty_record():
    tested = record.Record()
    assert tested == {}
