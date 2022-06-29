# Import Utils
from io import BytesIO
from PIL import Image
import os
import base64
import mimetypes
import re


def save_file(data, path):
    file_bytes = base64.b64decode(data)

    mime = mimetypes.guess_type(data)[0]
    extension = mimetypes.guess_extension(mime)
    file = open(f'{os.path.abspath(path)}\\filename{extension}', 'wb')
    file.write(file_bytes)
    file.close()

    # file = Image.open(base64.b64decode(file_bytes))
    # file.save(f'{os.path.abspath(path)}\\filename{extension}')
