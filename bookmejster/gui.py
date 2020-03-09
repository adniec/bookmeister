import tkinter as tk
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
        self.form.grid(row=0, column=0)


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
