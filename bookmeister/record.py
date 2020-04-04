"""#### Record

Module collecting functions, classes and methods needed for representation and validation of data which will be stored
in database. `VALUES` holds information about database keys, example values and accepted length of each field. Function
`cast_values` allows to change data types in dictionary (containing strings from `tkinter` entries) to those expected
in database. `Validator` class runs series of tests for data and notifies when values are incorrect. Modules used:
`dataclassess` and `datetime`.


#### License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime

from dataclasses import dataclass


def cast_values(values):
    """Casts values to proper type.

    Parameters
    ----------
    values : dict
        dictionary with names of fields and their values, it can contain only one position or each of them

    Examples
    --------
    >>> query = {"Pages": "50", "Price": "12.95"}
    >>> cast_values(query)
    >>> query
    {"Pages": 50, "Price": 12.95}
    """

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
    """Used to represent field stored in database. Covers key name, example value, accepted field min and max length."""

    name: str
    value: str
    range_min: int
    range_max: int

    def is_length_correct(self, value):
        """Specifies if value has acceptable length.

        Parameters
        ----------
        value : str
            text value which length will be checked

        Returns
        -------
        bool
            True if value length is between `range_min` and `range_max` of `Record` else False
        """

        return self.range_min <= len(value) <= self.range_max


VALUES = (
    Record('Title', 'From Russia, with Love', 1, 50),
    Record('Author', 'Ian Fleming', 3, 50),
    Record('Type', 'Thriller', 3, 20),
    Record('Publisher', 'Thomas and Mercer', 1, 30),
    Record('ISBN', '9781612185477', 13, 13),
    Record('Release', '2012', 4, 4),
    Record('Language', 'EN', 2, 2),
    Record('Pages', '181', 1, 4),
    Record('Quantity', '10', 1, 3),
    Record('Price', '125.50', 1, 6),
    Record('Discount', '0', 1, 2),
)


class Validator:
    """
    Responsible for validation of data.

    ...

    Attributes
    ----------
    is_correct : bool
        information about validation process
    numeric_fields : tuple
        names of numeric fields

    Methods
    -------
    warn(message, field=None)
        displays error window with passed message and clears set field, if None clears whole form

    Examples
    --------
    Check each value of all necessary fields in dictionary:
    >>> values = {
    ...     "Title": "From Russia, with Love",
    ...     "Author": "Ian Fleming",
    ...     "Type": "Thriller",
    ...     "Publisher": "Thomas and Mercer",
    ...     "ISBN": "9781612185477",
    ...     "Release": "2012",
    ...     "Language": "EN",
    ...     "Pages": "181",
    ...     "Quantity": "10",
    ...     "Price": "125.5",
    ...     "Discount": "0"
    ... }
    >>> validator = Validator(self.show_error)
    >>> validtor.process(values)
    >>> validator.is_correct
    True

    Check single field:
    >>> validator = Validator(self.show_error)
    >>> validtor.check_isbn("9781612185477")
    >>> validator.is_correct
    True
    """

    def __init__(self, show_error):
        """
        Parameters
        ----------
        show_error : method
            method from Gui to display error and clear proper field
        """

        self.is_correct = True
        self.numeric_fields = ('Pages', 'Quantity', 'Price', 'Discount')
        self.warn = show_error

    def process(self, data):
        """Checks fields from dictionary with data.

        Parameters
        ----------
        data : dict
            contains all keys necessary in database record and their values to check
        """

        for record in VALUES:
            self.check_length(record, data[record.name])
        for key in self.numeric_fields:
            self.check_number(data[key], key)
        self.check_isbn(data['ISBN'])
        self.check_release(data['Release'])

    def check_release(self, year):
        """Checks if value for field "Release" is correct.

        Tries to convert passed value to int and checks if it is between accepted values. If not sets `self.is_correct`
        to False and displays error.

        Parameters
        ----------
        year : str
            string to check if it is between accepted values
        """

        min = 1800
        max = datetime.now().year + 1
        try:
            if min <= int(year) <= max: return
        except ValueError:
            pass
        self.is_correct = False
        self.warn(f'Field "Release" must be a number between {min} and {max}.', 'Release')

    def check_isbn(self, number):
        """Checks if value for field "ISBN" is correct.

        Checks if passed value is digit and its length is equal to 13. Then runs calculations to compare result with
        checksum. If conditions are not met sets `self.is_correct` to False and displays error.

        Parameters
        ----------
        number : str
            string to check if it is correct ISBN-13 number
        """

        if number.isdigit() and len(number) == 13:
            n = [int(x) for x in number]
            control = (10 - ((n[0] + n[2] + n[4] + n[6] + n[8] + n[10] + 3 * (
                    n[1] + n[3] + n[5] + n[7] + n[9] + n[11])) % 10)) % 10
            if n[12] == control: return
        self.is_correct = False
        self.warn(f'Wrong value for ISBN-13 number.', 'ISBN')

    def check_number(self, value, field):
        """Checks if value for passed field is correct.

        Checks if value can be converted to float. If not sets `self.is_correct` to False and displays error.

        Parameters
        ----------
        value : str
            string to check if it can be converted to float
        field : str
            name of field which is checked
        """

        try:
            float(value)
        except ValueError:
            self.is_correct = False
            self.warn(f'Field "{field}" must be a number.', field)

    def check_length(self, record, value):
        """Checks if passed value has acceptable length for set record.

        If not sets `self.is_correct` to False and displays error.

        Parameters
        ----------
        record : Record
            class representing record with its name, example value and min, max accepted length
        value : str
            string to check if it has proper length
        """

        is_correct = record.is_length_correct(value)
        if not is_correct:
            text = self.get_length_text(record.range_min, record.range_max)
            self.warn(f'Length for field "{record.name}" must be {text} signs, e.g. {record.value}', record.name)
            self.is_correct = False

    @staticmethod
    def get_length_text(min: int, max: int) -> str:
        """Returns text according to min and max value."""

        if min == max:
            return f'exact {min}'
        return f'between {min} and {max}'
