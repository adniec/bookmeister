from bookmeister.gui import Gui
from sys import platform


def main():
    width = '450' if platform == 'win32' else '600'
    Gui('Bookstore Manager', f'{width}x470').mainloop()


if __name__ == '__main__': main()
