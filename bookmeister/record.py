"""#### Record

Module collecting functions necessary to validate data from application form.
Each of them raises `ValueError` when set value is not correct. Values are
supposed to be stored in class `Record` which extends dictionary and maps
proper validation function with expected database key. All database fields are
added to `FIELDS`. `datetime` module is used to acquire current year during
validation.


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

FIELDS = ('Title', 'Author', 'Type', 'Publisher', 'ISBN', 'Release',
          'Language', 'Pages', 'Quantity', 'Price', 'Discount')


def check_length(text, minimum=1, maximum=100):
    """Check if length of passed text is between set values.

    Parameters
    ----------
    text : str
        string to check if its length is in set range
    minimum : int
        minimum value for text length
    maximum : int
        maximum value for text length

    Raises
    ------
    ValueError
        when text length is not in range
    """
    if not minimum <= len(text) <= maximum:
        raise ValueError(f'Text length must be {minimum} to {maximum} '
                         'characters.')


def check_number(value, minimum=0, maximum=9999):
    """Check if passed string is integer between set values.

    Parameters
    ----------
    value : str
        string to check if it is integer in set range
    minimum : int
        minimum value for accepted number
    maximum : int
        maximum value for accepted number

    Raises
    ------
    ValueError
        when value cannot be converted to `int` or is not in range
    """
    try:
        number = int(value)
    except ValueError:
        raise ValueError('It must be integer.')

    if not minimum <= number <= maximum:
        raise ValueError(f'Number must be in range {minimum} to {maximum}.')


def check_isbn(number):
    """Check if ISBN-13 number is correct.

    Check if passed value is digit and its length is equal to 13. Then run
    calculations to compare result with checksum. If conditions are not met
    raise ValueError.

    Parameters
    ----------
    number : str
        string to check if it is correct ISBN-13 number

    Raises
    ------
    ValueError
        when value for ISBN-13 is not correct
    """
    if number.isdigit() and len(number) == 13:
        n = [int(char) for char in number]
        control = (10 - ((n[0] + n[2] + n[4] + n[6] + n[8] + n[10] + 3 * (
                n[1] + n[3] + n[5] + n[7] + n[9] + n[11])) % 10)) % 10
        if n[12] == control:
            return
    raise ValueError('Number must be valid ISBN-13 code.')


def check_lang_code(code):
    """Check if language code has two letters.

    Parameters
    ----------
    code : str
        string to check if it is correct language code

    Raises
    ------
    ValueError
        when value for language code is not correct
    """
    if not code.isalpha() or not len(code) == 2:
        raise ValueError(f'Language code must be two characters. '
                         'Check ISO 639-1 for more details.')


def check_price(value):
    """Check if passed string is price.

    Parameters
    ----------
    value : str
        string to check if it is int or float number with proper precision

    Raises
    ------
    ValueError
        when value contains letters or has too many digits after dot
    """
    price = value.split('.')
    try:
        if len(price) > 2:
            raise ValueError
        check_number(price[0])
        check_number(price[1], 0, 99)
    except IndexError:
        pass
    except ValueError:
        raise ValueError('Price must be a number with maximum two digits after'
                         ' dot, e.g. "125.75".')


class Record(dict):
    """
    Creates customized dictionary.

    It validates new elements if their keys are stored in `FIELDS`. Method
    `check` binds proper function needed for validation. It extends `dict`.
    """

    def __setitem__(self, key, value):
        """Extend `__setitem__` method by value check for `FIELDS` elements."""
        if key in FIELDS and isinstance(value, str):
            self.check(key, value)
        super(Record, self).__setitem__(key, value)

    @staticmethod
    def check(key, value):
        """Map functions which check field value with expected key."""
        if key in ('Title', 'Author', 'Type', 'Publisher'):
            check_length(value)
        elif key in ('Release', 'Pages', 'Quantity', 'Discount'):
            args = []
            if key == 'Release':
                args.extend((1800, datetime.now().year + 1))
            if key == 'Discount':
                args.extend((0, 99))
            check_number(value, *args)
        else:
            {'ISBN': check_isbn,
             'Language': check_lang_code,
             'Price': check_price}[key](value)

    def cast(self):
        """Cast `Record` values to type expected in database."""
        try:
            self['Price'] = float(self['Price'])
        except (KeyError, ValueError):
            pass

        for field in ('ISBN', 'Release', 'Pages', 'Quantity', 'Discount'):
            try:
                self[field] = int(self[field])
            except (KeyError, ValueError):
                pass
