"""GUI

Module gathers all functions, classes and methods necessary to create GUI. Its parts are divided for separate blocks
represented by classes `Search`, `Form`, `Buttons` and `Image` where each of them extends `tkinter.Frame`. `Searchbox`
is extended `tkinter.Combobox` class to application needs. `Gui` connects each part and places them in main window
which will be displayed. Modules used: `pathlib` and `tkinter` with `ttk`, `messagebox`, `filedialog`.


#### License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from tkinter.filedialog import askopenfile
from pathlib import Path
from bookmeister.record import VALUES, Validator, cast_values
from bookmeister.picture import Picture
from bookmeister.connection import Database


def show_no_connection():
    """Displays error message about connection problem."""

    msg.showerror('Error', 'Could not perform operation. It may be connection with database problem. Try again later.')


def create_label(container, message, row, column):
    """Displays text in set `tkinter` container.

    Parameters
    ----------
    container : tk.Tk or tk.Frame
        place where label will be bound
    message : str
        text displayed
    row : int
        row used with grid manager, specifies place where label will be displayed
    column : int
        column used with grid manager, specifies place where label will be displayed
    """

    tk.Label(container, text=message, font='none 10').grid(row=row, column=column, padx=12, pady=2, sticky='W')


class Gui(tk.Tk):
    """
    Configures GUI. Places individual widgets and allows their communication. Extends `tk.Tk`.

    ...

    Attributes
    ----------
    form : Form
        used for communication with `Form` widget
    search : Search
        used for communication with `Search` widget
    """

    def __init__(self, title, size):
        """
        Parameters
        ----------
        title : str
            name of application, displayed on top bar
        size : str
            application size in format 'heightxwidth'
        """

        super().__init__()
        self.title(title)
        self.geometry(size)
        self.resizable(0, 0)
        self.form = Form(self)
        self.form.grid(row=1, column=0)
        self.search = Search(self)
        self.search.grid(row=0, column=0, pady=15)
        Image(self).grid(row=2, column=0, padx=50, sticky='W')
        Buttons(self).grid(row=3, column=0, sticky='E')


class Search(tk.Frame):
    """
    Creates search widget. Extends `tk.Frame`.

    ...

    Attributes
    ----------
    box : Searchbox
        used for communication with `Searchbox`
    """

    def __init__(self, menu):
        """
        Parameters
        ----------
        menu : Gui
            container where `Search` widget will be bound, used to pass `Form` variables
        """

        super().__init__(menu)
        create_label(self, 'Search results:', 0, 0)
        self.box = Searchbox(self, menu.form.variables)
        self.box.grid(row=0, column=1)


class Searchbox(ttk.Combobox):
    """
    Creates searchbox. Extends `tk.Combobox`.

    ...

    Attributes
    ----------
    values : dict
        has keys as displayed text in `Searchbox` and values as dictionaries holding information about records
    variables : dict
        dictionary storing keys used in `Form` and corresponding to them `tk.StringVar`s, modifying its values change
        text seen in form
    """

    def __init__(self, frame, variables):
        """
        Parameters
        ----------
        frame : Search
            container where `Searchbox` will be bound
        variables : dict
            dictionary with `Form` variables
        """

        super().__init__(frame, width=50, state='readonly')
        self.values = {}
        self.variables = variables
        self.bind('<<ComboboxSelected>>', self.do_on_select)

    def assing_values(self, values):
        """Fills searchbox with values.

        Clears previously loaded elements. For each record in passed values creates text which is placed in searchbox.
        Stores it as key in `self.values` dictionary with corresponding it record values (dictionary). Then picks first
        record and fills form with its values.

        Parameters
        ----------
        values : list
            list with database records, their data stored in dictionaries
        """

        self.clear()
        try:
            for value in values:
                self.values[f'{value["ISBN"]} "{value["Title"]}" by {value["Author"]}'] = value
            self['values'] = sorted(list(self.values.keys()))
            self.current(0)
            self.do_on_select()
        except (TypeError, tk.TclError):
            msg.showwarning('No records', 'Could not find any results to set criteria.')

    def assign_image(self, image):
        """Stores image data in `self.values`.

        Parameters
        ----------
        image : str
            string representing image data converted with `bookmeister.picture` module
        """

        self.values[ttk.Combobox.get(self)]['Cover'] = image

    def do_on_select(self, *_):
        """Fills form with values from selected record."""

        for key in self.variables.keys():
            try:
                self.variables[key].set(self.values[ttk.Combobox.get(self)][key])
            except KeyError:
                pass

    def get(self):
        """Returns record id string when selected or None and displays error."""

        try:
            return self.values[ttk.Combobox.get(self)]['_id']
        except KeyError:
            msg.showerror('Error', 'No record selected. To perform operation please select record first.')

    def get_image(self):
        """Returns image data string when it exists else None."""

        try:
            return self.values[ttk.Combobox.get(self)]['Cover']
        except KeyError:
            return None

    def clear(self):
        """Clears positions from searchbox."""

        self.values.clear()
        self.set('')
        self['values'] = []


class Form(tk.Frame):
    """
    Creates form widget. Extends `tk.Frame`.

    ...

    Attributes
    ----------
    menu : Gui
        used to bind `Form` widget and communication with other menu elements
    variables : dict
        dictionary storing `tk.StringVar`s with corresponding them names as keys
    """

    def __init__(self, menu):
        super().__init__(menu)
        self.menu = menu
        self.variables = {}
        for place, record in enumerate(VALUES):
            create_label(self, f'{record.name}:', place, 0)
            self.create_entry(record.name, record.value, place, 1)
        tk.Button(self, text='Clear', width=4, command=self.clear).grid(row=place + 1, column=1, sticky='NE')
        self.create_checkbutton('Hardcover', place + 1, 0)

    def get(self):
        """Returns dictionary with fields names and their values."""

        return {key: value.get() for key, value in self.variables.items()}

    def clear(self):
        """Clears each variable value and removes records from `Searchbox`."""

        self.menu.search.box.clear()
        for variable in self.variables.values():
            try:
                variable.set('')
            except tk.TclError:
                variable.set(False)

    def create_checkbutton(self, name, row, column):
        """Displays checkbutton.

        Binds `tk.Checkbutton` to `Form` frame. Creates `tk.BooleanVar` and stores it in `self.variables`. Displays
        label with set name.

        Parameters
        ----------
        name : str
            text displayed before checkbutton, used as key in `self.variables`
        row : int
            row used with grid manager, specifies place where checkbutton will be displayed
        column : int
            column used with grid manager, specifies place where checkbutton will be displayed
        """

        create_label(self, f'{name}: ', row, column)
        content = tk.BooleanVar(self)
        tk.Checkbutton(self, variable=content).grid(row=row, column=column + 1, padx=3, sticky='W')
        self.variables[name] = content

    def create_entry(self, name, value, row, column):
        """Displays entry.

        Binds `tk.Entry` to `Form` frame. Creates `tk.StringVar` and stores it in `self.variables` with key passed in
        name.

        Parameters
        ----------
        name : str
            used as key in `self.variables`
        value : str
            default value displayed in entry on application startup
        row : int
            row used with grid manager, specifies place where entry will be displayed
        column : int
            column used with grid manager, specifies place where entry will be displayed
        """

        content = tk.StringVar(self, value=value)
        tk.Entry(self, width=40, textvariable=content).grid(row=row, column=column, padx=10, pady=2, sticky='W')
        self.variables[name] = content


class Image(tk.Frame):
    """
    Creates image widget. Extends `tk.Frame`.

    ...

    Attributes
    ----------
    menu : Gui
        used to bind `Image` widget and communication with other menu elements
    """

    def __init__(self, menu):
        super().__init__(menu)
        self.menu = menu
        tk.Button(self, text='Add cover', width=8, command=self.add_image).grid(row=0, column=0, pady=15)
        tk.Button(self, text='View cover', width=8, command=self.view_image).grid(row=0, column=1, sticky='W')

    def add_image(self):
        """Updates selected record image in database.

        When record is selected in `Searchbox` opens window where user can pick image file. Then converts image with
        `bookmeister.picture` module. If it succeed adds it to database else displays error window.
        """

        selected = self.menu.search.box.get()
        if selected:
            path = askopenfile(initialdir=Path.home())
            if path:
                image = Picture(path.name).get()
                if image:
                    if Database().update(selected, {'Cover': image}):
                        self.menu.search.box.assign_image(image)
                        msg.showinfo('Done', 'Record successfully saved to database.')
                    else:
                        show_no_connection()
                else:
                    msg.showerror('Error', 'Wrong image file format.')

    def view_image(self):
        """Displays selected record image.

        When record is selected in `Searchbox` opens its image with `bookmeister.picture` module. If operation failed
        displays error.
        """

        if self.menu.search.box.get():
            if not Picture.show(self.menu.search.box.get_image()):
                msg.showerror('Error', 'Could not open image. File may be corrupted or not uploaded yet.')


class Buttons(tk.Frame):
    """
    Creates buttons widget. Extends `tk.Frame`.

    ...

    Attributes
    ----------
    menu : Gui
        used to bind `Buttons` widget and communication with other menu elements
    """

    def __init__(self, menu):
        super().__init__(menu)
        self.menu = menu
        positions = ('add', 'search', 'revise', 'delete')
        for place, name in enumerate(positions):
            tk.Button(self, text=name.capitalize(), width=5, command=eval(f'self.{name}')).grid(row=0, column=place)

    def process_data(self, data, operation, *args):
        """Checks data and performs passed database operation.

        Uses `bookmeister.record.Validator.process` to check passed data. If they are correct
        `bookmeister.record.cast_values` to accepted format in database. Then sends them. Clears `Form`, `Searchbox`
        and notifies about success. In case of error displays proper message.

        Parameters
        ----------
        data : dict
            contains values collected from form fields
        operation : method
            operation performed on `bookmeister.connection.Database` - add or update
        *args
            used to pass record id for update operation
        """

        validator = Validator(self.show_error)
        validator.process(data)
        if validator.is_correct:
            cast_values(data)
            if operation(*args, data):
                msg.showinfo('Done', 'Record successfully saved to database.')
                self.menu.search.box.clear()
                self.menu.form.clear()
            else:
                show_no_connection()

    def add(self):
        """Adds record to database.

        Use `Form.get` to collect data. Then checks database if record with set ISBN number already exists. If not adds
        it. In case of errors displays notification. If succeed information is displayed aswell.
        """

        data = self.menu.form.get()
        exists = self.exist_check(data['ISBN'])
        if exists is None:
            show_no_connection()
        else:
            if exists:
                self.show_error('Record with set ISBN already exists in database.')
            else:
                self.process_data(data, Database().add)

    def search(self):
        """Search for record matching criteria in database.

        Use `Form.get` to collect values. Removes those taken from empty fields. If search parameters are specified then
        `bookmeister.record.cast_values` types to expected in database. Finally places request results in `Searchbox`.
        """

        parameters = {key: value for key, value in self.menu.form.get().items() if value}
        if parameters:
            cast_values(parameters)
            result = Database().search(parameters)
            if result is None:
                show_no_connection()
            else:
                self.menu.search.box.assing_values(result)

    def revise(self):
        """Update record in database.

        Use `Form.get` to collect values. Checks if record to update is selected in `Searchbox` then sends data.
        """

        data = self.menu.form.get()
        selected = self.menu.search.box.get()
        if selected:
            self.process_data(data, Database().update, selected)

    def delete(self):
        """Update record in database.

        Checks if record is selected in `Searchbox` then removes it from database. `Form` and `Searchbox` are cleared.
        Notification about success is displayed. In case of errors information is shown aswell.
        """

        selected = self.menu.search.box.get()
        if selected:
            if Database().delete(selected):
                msg.showinfo('Done', 'Record successfully removed from database.')
                self.menu.search.box.clear()
                self.menu.form.clear()
            else:
                show_no_connection()

    def exist_check(self, number):
        """Checks if record with set ISBN is already in database.

        Parameters
        ----------
        number : str
            string number taken from ISBN field

        Returns
        -------
        list
            with matching result to set number or empty
        None
            in case of connection error with database
        False
            when passed number is empty string ""
        """

        if number:
            query = {'ISBN': number}
            cast_values(query)
            return Database().search(query)
        return False

    def show_error(self, message, field=None):
        """Displays error window and clears form field (whole form when None field set).

        Parameters
        ----------
        message : str
            text displayed in error window
        field : str or None, optional
            name of field where value will be cleared, default None - clears whole form
        """

        if field is None:
            self.menu.form.clear()
        else:
            self.menu.form.variables[field].set('')
        msg.showerror('Error', message)
