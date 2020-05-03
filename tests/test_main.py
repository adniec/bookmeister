import pytest
from sys import platform

from bookmeister.__main__ import main
from bookmeister.gui import Gui


@pytest.mark.parametrize('size', (
        pytest.param('450x470', marks=pytest.mark.xfail(
            platform != 'win32', reason="Application size for Windows.")),
        pytest.param('600x470', marks=pytest.mark.xfail(
            platform == 'win32', reason="Application size not for Windows.")),
))
def test_launch_app(mocker, size):
    mocker.patch.object(Gui, 'mainloop')
    mocked = mocker.patch('bookmeister.__main__.Gui')
    main()
    mocked.assert_called_once_with('Bookstore Manager', size)
