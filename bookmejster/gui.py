import tkinter as tk
import tkinter.ttk as ttk
from bookmejster.record import VALUES


class Gui(tk.Tk):

    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.resizable(0, 0)
        self.variables = {}
        self.search_box = None
        self.create()

    def create(self):
        Search(self).grid(row=0, column=0, pady=15)
        Form(self).grid(row=1, column=0, pady=15)
        Buttons(self).grid(row=2, column=0, pady=15, sticky='E')

    def clear_form(self):
        for variable in self.variables.values():
            variable.set('')

    def create_label(self, message, row, column, container=None):
        if container is None:
            container = self
        tk.Label(container, text=message, font='none 10').grid(row=row, column=column, padx=12, pady=2, sticky='W')

    def add(self):
        pass

    def search(self):
        pass

    def revise(self):
        pass

    def add_image(self):
        pass

    def delete(self):
        pass


class Form(tk.Frame):

    def __init__(self, menu):
        super().__init__(menu)
        for place, record in enumerate(VALUES):
            menu.create_label(f'{record.name}:', place, 0, self)
            self.create_entry(menu, record.name, place, 1, record.value)
        tk.Button(self, text='Add cover', width=8, command=menu.add_image).grid(row=place + 1, column=0, pady=15)
        self.create_checkbutton(menu, 'Hardcover', place + 2, 0)

    def create_checkbutton(self, menu, name, row, column):
        content = tk.BooleanVar(menu)
        tk.Checkbutton(self, text=name, variable=content).grid(row=row, column=column, padx=5, sticky='W')
        menu.variables[name] = content

    def create_entry(self, menu, name, row, column, default=''):
        content = tk.StringVar(menu, value=default)
        tk.Entry(self, width=40, textvariable=content).grid(row=row, column=column, padx=10, pady=2, sticky='W')
        menu.variables[name] = content


class Search(tk.Frame):

    def __init__(self, menu):
        super().__init__(menu)
        menu.create_label('Search results:', 0, 0, self)
        menu.search_box = ttk.Combobox(self, width=50)
        menu.search_box.grid(row=0, column=1)


class Buttons(tk.Frame):

    def __init__(self, menu):
        super().__init__(menu)
        positions = ('add', 'search', 'revise', 'delete')
        for place, name in enumerate(positions):
            tk.Button(self, text=name.capitalize(), width=5, command=eval(f'menu.{name}')).grid(row=0, column=place)


