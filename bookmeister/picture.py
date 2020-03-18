"""Picture

Module created for processing image data. It encodes or decodes information about picture which will be send or is
received from database. Operations performed here ensure that data will be stored in proper form. Module responsible
for it is `base64`. To display image `PIL` and `io` are used.


#### License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from PIL import Image
import base64
import io


class Picture:
    """Responsible for picture encoding and decoding to provide format accepted in database."""

    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            path to image file which will be processed

        Attributes
        ----------
        _image : bytes or None
            bytes of loaded picture from set path or None in case of error
        """

        self._image = self.load(path)

    def get(self):
        """Encodes image from set path and converts to string.

        Returns
        -------
        str
            image information encoded with `base64`
        None
            when file from set path could not be opened by `PIL`
        """

        if self._image:
            return base64.encodebytes(self._image).decode()

    def load(self, path):
        """Opens and returns image bytes from set path.

        Parameters
        ----------
        path : str
            path of image to open

        Returns
        -------
        bytes
            image information
        None
            when file from set path could not be opened by `PIL`
        """

        try:
            with open(path, mode='rb') as img:
                image = img.read()
            Image.open(io.BytesIO(image))
            return image
        except (FileNotFoundError, OSError):
            return None

    @staticmethod
    def show(image_data):
        """Displays image.

        Uses encode method on passed string in `image_data` then decodebytes from `base64`. When image has proper format
        it displays it with `PIL` sending `BytesIO`.

        Parameters
        ----------
        image_data : str
            image information to decode and display

        Returns
        -------
        bool
            True when image is displayed, False when error occurs
        """

        try:
            image = base64.decodebytes(image_data.encode())
            Image.open(io.BytesIO(image)).show()
            return True
        except (FileNotFoundError, OSError, AttributeError):
            return False
