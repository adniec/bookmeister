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


@pytest.fixture
def cast_record(args):
    fields = ('Price', 'ISBN', 'Release', 'Pages', 'Quantity', 'Discount')
    tested = record.Record()
    for index, argument in enumerate(args):
        try:
            tested[fields[index]] = argument
        except ValueError:
            pass
    tested.cast()
    return tested


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


@pytest.mark.parametrize(('key', 'value', 'expected'), (
        ('Title', 'Test', {'Title': 'Test'}),
        ('Title', 'Test' * 50, {}),
        ('Author', 'Mr Test', {'Author': 'Mr Test'}),
        ('Type', 'Thriller', {'Type': 'Thriller'}),
        ('Publisher', 'Test' * 50, {}),
        ('Release', '2020', {'Release': '2020'}),
        ('Release', '1800', {'Release': '1800'}),
        ('Release', '1321', {}),
        ('Release', '2085', {}),
        ('Language', 'EN', {'Language': 'EN'}),
        ('Language', 'ES', {'Language': 'ES'}),
        ('Language', '12', {}),
        ('Language', 'E~', {}),
        ('Pages', '1651', {'Pages': '1651'}),
        ('Pages', '9999999', {}),
        ('Pages', '-158', {}),
        ('Quantity', '10', {'Quantity': '10'}),
        ('Quantity', 'Test', {}),
        ('Quantity', '-100', {}),
        ('Quantity', '45.5', {}),
        ('Price', '100', {'Price': '100'}),
        ('Price', '89.99', {'Price': '89.99'}),
        ('Price', '12.345', {}),
        ('Discount', '50', {'Discount': '50'}),
        ('Discount', '-15', {}),
        ('Discount', '2.5', {}),
        ('Discount', 'Test', {}),
        ('Title', '', {}),
        ('Author', '', {}),
        ('Type', '', {}),
        ('Publisher', '', {}),
        ('ISBN', '', {}),
        ('Publisher', '', {}),
        ('Release', '', {}),
        ('Language', '', {}),
        ('Pages', '', {}),
        ('Quantity', '', {}),
        ('Price', '', {}),
        ('Discount', '', {}),
        ('Test', 'Test', {'Test': 'Test'}),
))
def test_add_record_value(key, value, expected):
    tested = record.Record()
    try:
        tested[key] = value
    except ValueError:
        pass
    assert tested == expected


@pytest.mark.parametrize(('key', 'value'), (
        ('Title', 'Test' * 50),
        ('Author', 'Test' * 50),
        ('Type', 'Test' * 50),
        ('Publisher', 'Test' * 50),
        ('Release', 'Test' * 50),
        ('Language', 'Test'),
        ('Pages', '1000000'),
        ('Quantity', '-100'),
        ('Price', '12.345.6789'),
        ('Discount', '100'),
        ('Title', ''),
        ('Author', ''),
        ('Type', ''),
        ('Publisher', ''),
        ('ISBN', ''),
        ('Publisher', ''),
        ('Release', ''),
        ('Language', ''),
        ('Pages', ''),
        ('Quantity', ''),
        ('Price', ''),
        ('Discount', ''),
))
def test_record_raise_error(key, value):
    with pytest.raises(ValueError):
        tested = record.Record()
        tested[key] = value


@pytest.mark.parametrize(('args', 'expected'), (
        (('12.34', '9780330102360', '2005', '189', '10', '25'), {
            'Price': 12.34,
            'ISBN': 9780330102360,
            'Release': 2005,
            'Pages': 189,
            'Quantity': 10,
            'Discount': 25,
        }),
        (('123', '9781856132657', '1800', '-10', 'AB', '99'), {
            'Price': 123,
            'ISBN': 9781856132657,
            'Release': 1800,
            'Discount': 99,
        }),
        (('-10', 'test', '', '1580', '100', '5'), {
            'Pages': 1580,
            'Quantity': 100,
            'Discount': 5,
        }),
        (('100', '9780141028279', '1999'), {
            'Price': 100,
            'ISBN': 9780141028279,
            'Release': 1999,
        }),
        (('', '', '', '', '', '50'), {
            'Discount': 50,
        }),
        (('150.25', '9780099578031', '876', '762', '5'), {
            'Price': 150.25,
            'ISBN': 9780099578031,
            'Pages': 762,
            'Quantity': 5,
        }),
))
def test_record_cast_values(cast_record, expected):
    assert cast_record == expected
