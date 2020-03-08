from dataclasses import dataclass
from datetime import datetime


def cast_values(values):
    try:
        values['Price'] = float(values['Price'])
    except (KeyError, ValueError):
        pass

    for field in ('ISBN', 'Release', 'Pages', 'Quantity', 'Discount'):
        try:
            values[field] = int(values[field])
        except (KeyError, ValueError):
            pass


@dataclass(frozen=True)
class Record:
    name: str
    value: str
    range_min: int
    range_max: int

    def is_length_correct(self, value):
        return self.range_min <= len(value) <= self.range_max


VALUES = (
    Record('Title', 'From Russia, with Love', 1, 50),
    Record('Author', 'Ian Fleming', 3, 50),
    Record('Type', 'Thriller', 3, 20),
    Record('Publisher', 'Thomas and Mercer', 1, 30),
    Record('ISBN', '9781612185477', 13, 13),
    Record('Release', '2012', 4, 4),
    Record('Language', 'EN', 2, 2),  # ISO 639-1 Language Codes
    Record('Pages', '181', 1, 4),
    Record('Quantity', '10', 1, 3),
    Record('Price', '125.50', 1, 6),
    Record('Discount', '0', 1, 2),
)


class Validator:

    def __init__(self, show_error):
        self.is_correct = True
        self.numeric_fields = ('Pages', 'Quantity', 'Price', 'Discount')
        self.warn = show_error

    def process(self, data):
        for record in VALUES:
            self.check_length(record, data[record.name])
        for key in self.numeric_fields:
            self.check_number(data[key], key)
        self.check_isbn(data['ISBN'])
        self.check_release(data['Release'])

    def check_release(self, year):
        min = 1800
        max = datetime.now().year + 1
        try:
            if min <= int(year) <= max: return
        except ValueError:
            pass
        self.is_correct = False
        self.warn(f'Field "Release" must be a number between {min} and {max}.', 'Release')

    def check_isbn(self, number):
        if number.isalnum():
            n = [int(x) for x in number]
            control = (10 - ((n[0] + n[2] + n[4] + n[6] + n[8] + n[10] + 3 * (
                    n[1] + n[3] + n[5] + n[7] + n[9] + n[11])) % 10)) % 10
            if n[12] == control: return
        self.is_correct = False
        self.warn(f'Wrong value for ISBN-13 number.', 'ISBN')

    def check_number(self, value, field):
        try:
            float(value)
        except ValueError:
            self.is_correct = False
            self.warn(f'Field "{field}" must be a number.', field)

    def check_length(self, record, value):
        is_correct = record.is_length_correct(value)
        if not is_correct:
            text = self.get_lenght_text(record.range_min, record.range_max)
            self.warn(f'Length for field "{record.name}" must be {text} signs, e.g. {record.value}', record.name)
            self.is_correct = False

    @staticmethod
    def get_lenght_text(min, max):
        if min == max:
            return f'exact {min}'
        return f'between {min} and {max}'
