import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from bookmejster.record import VALUES


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
