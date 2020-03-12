import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from tkinter.filedialog import askopenfile
from pathlib import Path
from bookmeister.record import VALUES, Validator, cast_values
from bookmeister.image import show, get_image
from bookmeister.connection import Database


def show_no_connection():
    msg.showerror('Error', 'Could not perform operation. It may be connection with database problem. Try again later.')


def create_label(container, message, row, column):
    tk.Label(container, text=message, font='none 10').grid(row=row, column=column, padx=12, pady=2, sticky='W')


class Gui(tk.Tk):

    def __init__(self, title, size):
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

    def __init__(self, menu):
        super().__init__(menu)
        create_label(self, 'Search results:', 0, 0)
        self.box = Searchbox(self, menu.form.variables)
        self.box.grid(row=0, column=1)


class Searchbox(ttk.Combobox):

    def __init__(self, frame, variables):
        super().__init__(frame, width=50, state='readonly')
        self.values = {}
        self.variables = variables
        self.bind('<<ComboboxSelected>>', self.do_on_select)

    def assing_values(self, values):
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
        self.values[ttk.Combobox.get(self)]['Cover'] = image

    def do_on_select(self, *_):
        for key in self.variables.keys():
            try:
                self.variables[key].set(self.values[ttk.Combobox.get(self)][key])
            except KeyError:
                pass

    def get(self):
        try:
            return self.values[ttk.Combobox.get(self)]['_id']
        except KeyError:
            msg.showerror('Error', 'No record selected. To perform operation please select record first.')

    def get_image(self):
        try:
            return self.values[ttk.Combobox.get(self)]['Cover']
        except KeyError:
            return None

    def clear(self):
        self.values.clear()
        self.set('')
        self['values'] = []


class Form(tk.Frame):

    def __init__(self, menu):
        super().__init__(menu)
        self.menu = menu
        self.variables = {}
        for place, record in enumerate(VALUES):
            create_label(self, f'{record.name}:', place, 0)
            self.create_entry(record.name, place, 1)
        tk.Button(self, text='Clear', width=4, command=self.clear).grid(row=place + 1, column=1, sticky='NE')
        self.create_checkbutton('Hardcover', place + 1, 0)

    def get(self):
        return {key: value.get() for key, value in self.variables.items()}

    def clear(self):
        self.menu.search.box.clear()
        for variable in self.variables.values():
            try:
                variable.set('')
            except tk.TclError:
                variable.set(False)

    def create_checkbutton(self, name, row, column):
        create_label(self, f'{name}: ', row, column)
        content = tk.BooleanVar(self)
        tk.Checkbutton(self, variable=content).grid(row=row, column=column + 1, padx=3, sticky='W')
        self.variables[name] = content

    def create_entry(self, name, row, column):
        content = tk.StringVar(self)
        tk.Entry(self, width=40, textvariable=content).grid(row=row, column=column, padx=10, pady=2, sticky='W')
        self.variables[name] = content


class Image(tk.Frame):
    def __init__(self, menu):
        super().__init__(menu)
        self.menu = menu
        tk.Button(self, text='Add cover', width=8, command=self.add_image).grid(row=0, column=0, pady=15)
        tk.Button(self, text='View cover', width=8, command=self.view_image).grid(row=0, column=1, sticky='W')

    def add_image(self):
        selected = self.menu.search.box.get()
        if selected:
            path = askopenfile(initialdir=Path.home())
            if path:
                image = get_image(path.name)
                if image:
                    if Database().update(selected, {'Cover': image}):
                        self.menu.search.box.assign_image(image)
                        msg.showinfo('Done', 'Record successfully saved to database.')
                    else:
                        show_no_connection()
                else:
                    msg.showerror('Error', 'Wrong image file format.')

    def view_image(self):
        if self.menu.search.box.get():
            if not show(self.menu.search.box.get_image()):
                msg.showerror('Error', 'Could not open image. File may be corrupted or not uploaded yet.')


class Buttons(tk.Frame):

    def __init__(self, menu):
        super().__init__(menu)
        self.menu = menu
        positions = ('add', 'search', 'revise', 'delete')
        for place, name in enumerate(positions):
            tk.Button(self, text=name.capitalize(), width=5, command=eval(f'self.{name}')).grid(row=0, column=place)

    def process_data(self, data, operation, *args):
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
        parameters = {key: value for key, value in self.menu.form.get().items() if value}
        if parameters:
            cast_values(parameters)
            result = Database().search(parameters)
            if result is None:
                show_no_connection()
            else:
                self.menu.search.box.assing_values(result)

    def revise(self):
        data = self.menu.form.get()
        selected = self.menu.search.box.get()
        if selected:
            self.process_data(data, Database().update, selected)

    def delete(self):
        selected = self.menu.search.box.get()
        if selected:
            if Database().delete(selected):
                msg.showinfo('Done', 'Record successfully removed from database.')
                self.menu.search.box.clear()
                self.menu.form.clear()
            else:
                show_no_connection()

    def show_error(self, message, field=None):
        if field is None:
            self.menu.form.clear()
        else:
            self.menu.form.variables[field].set('')
        msg.showerror('Error', message)

    def exist_check(self, number):
        if number:
            query = {'ISBN': number}
            cast_values(query)
            return Database().search(query)
        return False
