from sys import platform
from pathlib import Path
from PyInstaller import __main__ as Install

Install.run([
    '--name=Bookmeister',
    '--onefile',
    '--windowed',
    f'--add-data={Path("bookmeister/bookmeister.png")}{";" if platform == "win32" else ":"}.',
    f'--icon={Path("data/bookmeister.ico")}',
    str(Path('bookmeister/').resolve() / '__main__.py'),
])
