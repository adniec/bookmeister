import pathlib
import pytest
from tkinter import TclError

from bookmeister import gui

RECORD = {
    'Title': 'Test me',
    'Author': 'Mr Test',
    'Type': 'Test',
    'Publisher': 'Tester',
    'ISBN': 9780340425626,
    'Release': 2020,
    'Language': 'EN',
    'Pages': 999,
    'Quantity': 123,
    'Price': 5.75,
    'Discount': 5,
    'Hardcover': False
}


def test_create_label(mocker):
    mocked = mocker.patch('tkinter.Label')
    gui.create_label(None, 'Hello', 1, 1)
    mocked.assert_called_once_with(None, text='Hello', font='none 10')


def test_show_no_connection(mocker):
    mocked = mocker.patch('tkinter.messagebox.showerror')
    gui.show_no_connection()
    mocked.assert_called_once()


@pytest.mark.parametrize('parameter,method', (
        (None, 'form.clear.called'),
        ('Title', 'form.variables["Title"].set.called')
))
def test_show_error(parameter, method, mocker):
    mocked = mocker.patch('tkinter.messagebox.showerror')
    mock = mocker.MagicMock()
    gui.Gui.show_error(mock, 'Error', parameter)
    assert getattr(mock, method)
    mocked.assert_called_once()


def test_get_icon_path():
    path = gui.Gui.get_icon()
    assert isinstance(path, pathlib.PurePath)

@pytest.mark.gui_init
@pytest.mark.parametrize('frame', (
        'bookmeister.gui.Form',
        'bookmeister.gui.Search',
        'bookmeister.gui.Image',
        'bookmeister.gui.Buttons',
))
def test_gui_init_frames(frame, mocker):
    mocker.patch('tkinter.Tk.iconphoto')
    mocked = mocker.patch(frame)
    gui.Gui('Hello', '100x100')
    mocked.assert_called_once()


def test_search_frame_init(mocker):
    mocked_label = mocker.patch('tkinter.Label')
    mocked_box = mocker.patch('bookmeister.gui.Searchbox')
    gui.Search(mocker.MagicMock())
    mocked_label.assert_called_once()
    mocked_box.assert_called_once()


def test_searchbox_frame_init(mocker):
    mocked = mocker.patch('tkinter.Widget.bind')
    box = gui.Searchbox(mocker.MagicMock(), {})
    mocked.assert_called_once()
    assert box.values == {}
    assert box.variables == {}


def test_searchbox_assign_no_values(mocker):
    mocked = mocker.patch('tkinter.messagebox.showwarning')
    gui.Searchbox.assign_values(mocker.MagicMock(), None)
    mocked.assert_called_once()


def test_searchbox_assign_values(mocker):
    mock = mocker.MagicMock()
    gui.Searchbox.assign_values(mock, [RECORD])
    mock.clear.assert_called_once()
    mock.values.__setitem__.assert_called_once_with(
        '9780340425626 "Test me" by Mr Test', RECORD)
    mock.do_on_select.assert_called_once()


def test_searchbox_assign_image_connects_with_combobox(mocker):
    mocked = mocker.patch('tkinter.ttk.Combobox.get')
    gui.Searchbox.assign_image(mocker.MagicMock(), '5fc00c0d')
    mocked.assert_called_once()


def test_searchbox_do_on_select_connects_with_combobox(mocker):
    mocked = mocker.patch('tkinter.ttk.Combobox.get')
    mock = mocker.MagicMock()
    mock.variables.keys.return_value = '.'
    gui.Searchbox.do_on_select(mock)
    mocked.assert_called_once()


def test_searchbox_get_error(mocker):
    mocked = mocker.patch('tkinter.messagebox.showerror')
    mocked_box = mocker.patch('tkinter.ttk.Combobox.get')
    mocked_box.side_effect = KeyError()
    gui.Searchbox.get(mocker.MagicMock())
    mocked.assert_called_once()


def test_searchbox_get_connects_with_combobox(mocker):
    mocked = mocker.patch('tkinter.ttk.Combobox.get')
    gui.Searchbox.get(mocker.MagicMock())
    mocked.assert_called_once()


def test_searchbox_get_image_error(mocker):
    mocked = mocker.patch('tkinter.ttk.Combobox.get')
    mocked.side_effect = KeyError()
    assert gui.Searchbox.get_image(mocker.MagicMock()) is None


def test_searchbox_get_image_connects_with_combobox(mocker):
    mocked = mocker.patch('tkinter.ttk.Combobox.get')
    gui.Searchbox.get_image(mocker.MagicMock())
    mocked.assert_called_once()


def test_searchbox_clear(mocker):
    mock = mocker.MagicMock()
    gui.Searchbox.clear(mock)
    mock.values.clear.assert_called_once()
    mock.set.assert_called_once()


def test_form_frame_init(mocker):
    mocked_label = mocker.patch('tkinter.Label')
    mocked_button = mocker.patch('tkinter.Button')
    mocked_entry = mocker.patch('bookmeister.gui.Form.create_entry')
    mocked_check = mocker.patch('bookmeister.gui.Form.create_checkbutton')
    mock = mocker.MagicMock()
    gui.Form(mock)
    mocked_label.assert_called()
    mocked_button.assert_called_once()
    mocked_entry.assert_called()
    mocked_check.assert_called_once()


def test_form_frame_get(mocker):
    mock = mocker.MagicMock()
    record = {}
    for key, value in RECORD.items():
        mocked = mocker.MagicMock()
        mocked.get.return_value = value
        record[key] = mocked
    mock.variables.items.return_value = record.items()
    assert gui.Form.get(mock, True) == RECORD


def test_form_frame_get_error(mocker):
    mocked = mocker.MagicMock()
    mock = mocker.MagicMock()
    mock.get.side_effect = ValueError()
    record = {'Title': mock}
    mocked.variables.items.return_value = record.items()
    gui.Form.get(mocked)
    mocked.menu.show_error.assert_called_once()


@pytest.mark.parametrize('parameter', ('', False,))
def test_form_frame_clear(parameter, mocker):
    mocked = mocker.MagicMock()
    mock = mocker.MagicMock()
    if isinstance(parameter, bool):
        mock.set.side_effect = [TclError(), None]
    mocked.variables.values.return_value = [mock]
    gui.Form.clear(mocked)
    mocked.menu.search.box.clear.assert_called_once()
    mock.set.assert_called_with(parameter)


def test_add_image(mocker):
    mocker.patch('bookmeister.gui.askopenfile')
    mocker.patch('bookmeister.connection.Database.upload_image')
    mocker.patch('bookmeister.connection.Database.update')
    mocked = mocker.patch('tkinter.messagebox.showinfo')
    gui.Image.add_image(mocker.MagicMock())
    mocked.assert_called_once()


def test_add_image_no_connection(mocker):
    mocker.patch('bookmeister.gui.askopenfile')
    mocked = mocker.patch('tkinter.messagebox.showerror')
    mock = mocker.MagicMock()
    mock.verify.return_value = False
    gui.Image.add_image(mock)
    mocked.assert_called_once()


def test_add_image_wrong_format(mocker):
    mocker.patch('bookmeister.gui.askopenfile')
    mocker.patch('bookmeister.connection.Database.upload_image')
    mocked = mocker.patch('bookmeister.gui.show_no_connection')
    mock = mocker.patch('bookmeister.connection.Database.update')
    mock.return_value = None
    gui.Image.add_image(mocker.MagicMock())
    mocked.assert_called_once()



def test_view_image(mocker):
    mocked = mocker.MagicMock()
    mocked.menu.search.box.get_image.return_value = True
    gui.Image.view_image(mocked)
    mocked.open_image.assert_called_once()


def test_view_no_image(mocker):
    mocked = mocker.patch('tkinter.messagebox.showerror')
    mock = mocker.MagicMock()
    mock.menu.search.box.get_image.return_value = False
    gui.Image.view_image(mock)
    mocked.assert_called_once()


def test_open_image(mocker):
    mocked = mocker.patch('webbrowser.open')
    gui.Image.open_image('test')
    mocked.assert_called_once()


@pytest.mark.parametrize('name,result', (
        ('bookmeister.png', True),
        ('test.png', False),
))
def test_image_verify(name, result):
    assert gui.Image.verify('bookmeister/' + name) == result


def test_buttons_process_wrong_data(mocker):
    mocked = mocker.patch('bookmeister.gui.show_no_connection')
    gui.Buttons.process_data(mocker.MagicMock(), RECORD, lambda x: None)
    mocked.assert_called_once()


def test_buttons_add_no_connection(mocker):
    mocked = mocker.patch('bookmeister.gui.show_no_connection')
    mock = mocker.MagicMock()
    mock.exist_check.return_value = None
    gui.Buttons.add(mock)
    mocked.assert_called_once()


def test_buttons_add_existing_record(mocker):
    mock = mocker.MagicMock()
    mock.exist_check.return_value = True
    gui.Buttons.add(mock)
    mock.menu.show_error.assert_called_once()


def test_buttons_search_no_connection(mocker):
    mocked = mocker.patch('bookmeister.gui.show_no_connection')
    mock = mocker.patch('bookmeister.connection.Database.search')
    mock.return_value = None
    gui.Buttons.search(mocker.MagicMock())
    mocked.assert_called_once()


def test_buttons_delete_no_connection(mocker):
    mocked = mocker.patch('bookmeister.gui.show_no_connection')
    mock = mocker.patch('bookmeister.connection.Database.delete')
    mock.return_value = None
    gui.Buttons.delete(mocker.MagicMock())
    mocked.assert_called_once()


def test_buttons_exist_check_no_number():
    assert gui.Buttons.exist_check(None) == False
