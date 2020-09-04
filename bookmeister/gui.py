"""#### GUI

Module gathers all functions, classes and methods necessary to create GUI. Its
parts are divided for separate blocks represented by classes `Search`, `Form`,
`Buttons` and `Image` where each of them extends `tkinter.Frame`. `Searchbox`
is extended `tkinter.Combobox` class to application needs. `Gui` connects each
part and places them in main window which will be displayed. Modules used:
`pathlib`, `sys`, `webbrowser`, `PIL` and `tkinter` with `filedialog`,
`messagebox`, `ttk`.


#### License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pathlib import Path
import sys
import tkinter as tk
from tkinter.filedialog import askopenfile
import tkinter.messagebox as msg
import tkinter.ttk as ttk
import webbrowser

import PIL
import PIL.Image

from bookmeister.connection import Database
from bookmeister.record import FIELDS, Record


def show_no_connection():
    """Display error message about connection problem."""
    msg.showerror('Error', 'Could not perform operation. It may be connection '
                           'with database problem. Try again later.')


def create_label(container, message, row, column):
    """Display text in set `tkinter` container.

    Parameters
    ----------
    container : tk.Tk or tk.Frame
        place where label will be bound
    message : str
        text displayed
    row : int
        row used with grid manager (place where label will be displayed)
    column : int
        column used with grid manager (place where label will be displayed)
    """
    tk.Label(container, text=message, font='none 10').grid(
        row=row, column=column, padx=12, pady=2, sticky='W')


class Gui(tk.Tk):
    """
    Configure GUI.

    Place individual widgets and allow their communication. Extend `tk.Tk`.

    ...

    Attributes
    ----------
    form : Form
        used for communication with `Form` widget
    search : Search
        used for communication with `Search` widget
    """

    def __init__(self, title, size):
        """Set window properties and fill it with elements.

        Parameters
        ----------
        title : str
            name of application, displayed on top bar
        size : str
            application size in format 'heightxwidth'
        """
        super().__init__(className=title)
        self.title(title)
        self.geometry(size)
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file=self.get_icon()))
        self.form = Form(self)
        self.form.grid(row=1, column=0)
        self.search = Search(self)
        self.search.grid(row=0, column=0, pady=15)
        Image(self).grid(row=2, column=0, padx=50, sticky='W')
        Buttons(self).grid(row=3, column=0, sticky='E')

    def show_error(self, message, field=None):
        """Display error window.

        When field is specified incorrect form value from that field is
        cleared. Otherwise clear whole form.

        Parameters
        ----------
        message : str
            text displayed in error window
        field : str or None, optional
            name of field where value will be cleared, default None: whole form
        """
        if field is None:
            self.form.clear()
        else:
            self.form.variables[field].set('')
            message = f'Wrong value for field "{field}". {message}'
        msg.showerror('Error', message)

    @staticmethod
    def get_icon():
        """Get icon path.

        According to type of installation pick method to get icon path. It can
        be obtained from module directory or from `_MEIPASS` when application
        is built.

        Returns
        -------
        Path
            `pathlib.Path` object containing information about icon path
        """
        directory = getattr(sys, '_MEIPASS', Path(__file__).parent.absolute())
        icon_path = Path(directory) / 'bookmeister.png'
        return icon_path


class Search(tk.Frame):
    """
    Create search widget. Extend `tk.Frame`.

    ...

    Attributes
    ----------
    box : Searchbox
        used for communication with `Searchbox`
    """

    def __init__(self, menu):
        """Create search bar elements.

        Parameters
        ----------
        menu : Gui
            container where `Search` widget will be bound, used to pass `Form`
            variables
        """
        super().__init__(menu)
        create_label(self, 'Search results:', 0, 0)
        self.box = Searchbox(self, menu.form.variables)
        self.box.grid(row=0, column=1)


class Searchbox(ttk.Combobox):
    """
    Create searchbox. Extend `tk.Combobox`.

    ...

    Attributes
    ----------
    values : dict
        has keys as displayed text in `Searchbox` and values as dictionaries
        holding information about records
    variables : dict
        dictionary storing keys used in `Form` and corresponding to them
        `tk.StringVar`s, modifying its values change text seen in form
    """

    def __init__(self, frame, variables):
        """Configure searchbox.

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

    def assign_values(self, values):
        """Fill searchbox with values.

        Clear previously loaded elements. For each record in passed values
        create text which is placed in searchbox. Store it as key in
        `self.values` dictionary with corresponding it record values
        (dictionary). Then pick first record and fill form with its values.

        Parameters
        ----------
        values : list
            list with database records, their data stored in dictionaries
        """
        self.clear()
        try:
            for data in values:
                title = f'{data["ISBN"]} "{data["Title"]}" by {data["Author"]}'
                self.values[title] = data
            self['values'] = sorted(list(self.values.keys()))
            self.current(0)
            self.do_on_select()
        except (TypeError, tk.TclError):
            msg.showwarning('No records',
                            'Could not find any results to set criteria.')

    def assign_image(self, image):
        """Store image data in `self.values`.

        Parameters
        ----------
        image : str
            string representing image id
        """
        self.values[ttk.Combobox.get(self)]['Cover'] = image

    def do_on_select(self, *_):
        """Fill form with values from selected record."""
        for key in self.variables.keys():
            try:
                self.variables[key].set(
                    self.values[ttk.Combobox.get(self)][key])
            except KeyError:  # pragma: no cover
                pass

    def get(self):
        """Return record id string when selected or None and display error."""
        try:
            return self.values[ttk.Combobox.get(self)]['_id']
        except KeyError:
            msg.showerror('Error', 'No record selected. To perform operation '
                                   'please select record first.')

    def get_image(self):
        """Return image id when it exists else None."""
        try:
            return self.values[ttk.Combobox.get(self)]['Cover']
        except KeyError:
            return None

    def clear(self):
        """Clear positions from searchbox."""
        self.values.clear()
        self.set('')
        self['values'] = []


class Form(tk.Frame):
    """
    Create form widget. Extend `tk.Frame`.

    ...

    Attributes
    ----------
    menu : Gui
        used to bind `Form` widget and communication with other menu elements
    variables : dict
        storing `tk.StringVar`s with corresponding them names as keys
    """

    def __init__(self, menu):
        """Configure form widget."""
        super().__init__(menu)
        self.menu = menu
        self.variables = {}
        for place, name in enumerate(FIELDS):
            create_label(self, f'{name}:', place, 0)
            self.create_entry(name, '', place, 1)
        tk.Button(self, text='Clear', width=4, command=self.clear).grid(
            row=place + 1, column=1, sticky='NE')
        self.create_checkbutton('Hardcover', place + 1, 0)

    def get(self, silent=False):
        """Return dictionary with fields names and their values from form.

        Values are cast to types expected in database. When `silent` is set to
        `False` display error window in case of incorrect field value.

        Parameters
        ----------
        silent : bool, optional
            specifies if error windows are shown or not in case of wrong values
        """
        record = Record()
        for key, value in self.variables.items():
            try:
                record[key] = value.get()
            except ValueError as error:
                if not silent:
                    self.menu.show_error(error, key)
        record.cast()
        return record

    def clear(self):
        """Clear each variable value and remove records from `Searchbox`."""
        self.menu.search.box.clear()
        for variable in self.variables.values():
            try:
                variable.set('')
            except tk.TclError:
                variable.set(False)

    def create_checkbutton(self, name, row, column):
        """Display checkbutton.

        Bind `tk.Checkbutton` to `Form` frame. Create `tk.BooleanVar` and store
         it in `self.variables`. Display label with set name.

        Parameters
        ----------
        name : str
            text displayed before checkbutton, used as key in `self.variables`
        row : int
            row used with grid manager (place where button will be shown)
        column : int
            column used with grid manager (place where button will be shown)
        """
        create_label(self, f'{name}: ', row, column)
        content = tk.BooleanVar(self)
        tk.Checkbutton(self, variable=content).grid(
            row=row, column=column + 1, padx=3, sticky='W')
        self.variables[name] = content

    def create_entry(self, name, value, row, column):
        """Display entry.

        Bind `tk.Entry` to `Form` frame. Create `tk.StringVar` and store it in
        `self.variables` with key passed in name.

        Parameters
        ----------
        name : str
            used as key in `self.variables`
        value : str
            default value displayed in entry on application startup
        row : int
            row used with grid manager (place where entry will be displayed)
        column : int
            column used with grid manager (place where entry will be displayed)
        """
        content = tk.StringVar(self, value=value)
        tk.Entry(self, width=40, textvariable=content).grid(
            row=row, column=column, padx=10, pady=2, sticky='W')
        self.variables[name] = content


class Image(tk.Frame):
    """
    Create image widget. Extend `tk.Frame`.

    ...

    Attributes
    ----------
    menu : Gui
        used to bind `Image` widget and communication with other menu elements
    """

    def __init__(self, menu):
        """Create buttons for interaction with images."""
        super().__init__(menu)
        self.menu = menu
        tk.Button(self, text='Add cover', width=8,
                  command=self.add_image).grid(row=0, column=0, pady=15)
        tk.Button(self, text='View cover', width=8,
                  command=self.view_image).grid(row=0, column=1, sticky='W')

    def add_image(self):
        """Update selected record image in database.

        When record is selected in `Searchbox` open window where user can pick
        image file. Then convert image with `bookmeister.picture` module. If
        it succeed add it to database else display error window.
        """
        selected = self.menu.search.box.get()
        if selected:
            path = askopenfile(initialdir=Path.home())
            if path:
                if self.verify(path.name):
                    image_id = Database().upload_image(path.name)
                    if image_id:
                        if Database().update(selected, {'Cover': image_id}):
                            self.menu.search.box.assign_image(image_id)
                            msg.showinfo('Done',
                                         'Image successfully saved.')
                        else:
                            show_no_connection()
                else:
                    msg.showerror('Error', 'Wrong image file format.')

    def view_image(self):
        """Display selected record image.

        When record is selected in `Searchbox` open its image in browser. If
        operation failed display error.
        """
        if self.menu.search.box.get():
            picture = self.menu.search.box.get_image()
            if picture:
                self.open_image(picture)
            else:
                msg.showerror('Error', 'There is no image uploaded yet.')

    @staticmethod
    def open_image(link):
        """Open image from database media archive in browser.

        Parameters
        ----------
        link : str
            identification number of image from database media archive
        """
        url = Database().url + '/media/' + link
        webbrowser.open(url, new=True)

    @staticmethod
    def verify(path):
        """Return True if under set path there is valid image else False."""
        try:
            image = PIL.Image.open(path)
            image.verify()
            image.close()
            return True
        except (FileNotFoundError, PIL.UnidentifiedImageError):
            return False


class Buttons(tk.Frame):
    """
    Create buttons widget. Extend `tk.Frame`.

    ...

    Attributes
    ----------
    menu : Gui
        used to bind `Buttons` widget and communication with other elements
    """

    def __init__(self, menu):
        """Create buttons for interaction with database."""
        super().__init__(menu)
        self.menu = menu
        positions = ('add', 'search', 'revise', 'delete')
        for place, name in enumerate(positions):
            tk.Button(self, text=name.capitalize(), width=5,
                      command=getattr(self, name)).grid(row=0, column=place)

    def process_data(self, data, operation, *args):
        """Check data and perform passed database operation.

        Check if passed dictionary has all necessary keys. If yes send them
        to database. Then clear `Form`, `Searchbox` and notify about success.
        In case of error display proper message.

        Parameters
        ----------
        data : dict
            contains values collected from form fields
        operation : method
            operation performed on `bookmeister.connection.Database`
        *args
            used to pass record id for update operation
        """
        if not set(FIELDS) - (data.keys()):
            if operation(*args, data):
                msg.showinfo('Done', 'Record successfully saved to database.')
                self.menu.search.box.clear()
                self.menu.form.clear()
            else:
                show_no_connection()

    def add(self):
        """Add record to database.

        Use `Form.get` to collect data. Then check database if record with set
        ISBN number already exists. If not add it. In case of errors display
        notification. If operation succeed information is displayed as well.
        """
        data = self.menu.form.get()
        exists = self.exist_check(data.get('ISBN', None))
        if exists is None:
            show_no_connection()
        else:
            if exists:
                self.menu.show_error(
                    'Record with set ISBN already exists in database.')
            else:
                self.process_data(data, Database().add)

    def search(self):
        """Search for record matching criteria in database.

        Use `Form.get` to collect values. Silent parameter is set to not
        display notifications about empty fields. Place request results in
        `Searchbox`.
        """
        parameters = self.menu.form.get(True)
        if parameters:
            result = Database().search(parameters)
            if result is None:
                show_no_connection()
            else:
                self.menu.search.box.assign_values(result)

    def revise(self):
        """Update record in database.

        Use `Form.get` to collect values. Check if record to update is selected
         in `Searchbox` then send data.
        """
        data = self.menu.form.get()
        selected = self.menu.search.box.get()
        if selected:
            self.process_data(data, Database().update, selected)

    def delete(self):
        """Remove record from database.

        Check if record is selected in `Searchbox` then removes it from
        database. `Form` and `Searchbox` are cleared. Notification about
        success is displayed. In case of errors information is shown as well.
        """
        selected = self.menu.search.box.get()
        if selected:
            if Database().delete(selected):
                msg.showinfo('Done',
                             'Record successfully removed from database.')
                self.menu.search.box.clear()
                self.menu.form.clear()
            else:
                show_no_connection()

    @staticmethod
    def exist_check(number):
        """Check if record with set ISBN is already in database.

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
            when passed number is empty string
        """
        if number:
            return Database().search({'ISBN': number})
        return False
