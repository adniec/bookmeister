"""Main

Contains `main` function which creates application GUI and sets its size. It needs module sys to specify which platform
is used and adjust application width.


#### License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from bookmeister.gui import Gui
from sys import platform


def main():
    """Sets GUI width according to used platform and runs it."""

    width = '450' if platform == 'win32' else '600'
    Gui('Bookstore Manager', f'{width}x470').mainloop()


if __name__ == '__main__': main()
