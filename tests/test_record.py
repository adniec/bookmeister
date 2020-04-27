from bookmeister.record import Validator
from pytest import fixture, mark


@fixture
def validator():
    return Validator(print)


def test_initialization(validator):
    assert validator.is_correct
    assert validator.numeric_fields == ('Pages', 'Quantity',
                                        'Price', 'Discount')
    assert callable(validator.warn)


@mark.parametrize(('year', 'expected'), ((1800, True),
                                         ('1847', True),
                                         (1978, True),
                                         ('2001', True),
                                         (2019, True),
                                         ('2020', True),
                                         (2021, True),
                                         (2004.1234, True),
                                         (2052, False),
                                         ('1742', False),
                                         ('1402', False),
                                         ('test', False),
                                         ('', False),
                                         (1600.4, False),
                                         (123456789, False),
                                         (1799, False),
                                         ))
def test_release_check(year, expected):
    tested = Validator(print)
    tested.check_release(year)
    assert tested.is_correct == expected


@mark.parametrize(('number', 'expected'), (('9780330102360', True),
                                           ('9781856132657', True),
                                           ('9780141028279', True),
                                           ('9780099578031', True),
                                           ('9780141190419', True),
                                           ('9780515055160', True),
                                           ('9780340425626', True),
                                           ('1234567890123', False),
                                           ('0123012301230', False),
                                           ('781856132657', False),
                                           ('1413304540', False),
                                           ('1932982118', False),
                                           ('01010101101', False),
                                           ('', False),
                                           ))
def test_isbn_check(number, expected):
    tested = Validator(print)
    tested.check_isbn(number)
    assert tested.is_correct == expected


@mark.parametrize(('number', 'expected'), (('12', True),
                                           ('1234567890', True),
                                           ('0123', True),
                                           ('456.789', True),
                                           ('10.5', True),
                                           ('-12', False),
                                           ('a10', False),
                                           ('1a', False),
                                           ('test', False),
                                           ('', False),
                                           ))
def test_number_check(number, expected):
    tested = Validator(print)
    tested.check_number(number, '')
    assert tested.is_correct == expected
