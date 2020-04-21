__author__ = 'deadblue'

import logging
import os
import io

from PIL import ImageFont

_logger = logging.getLogger(__name__)

def _load_font():
    font_file = os.path.join(
        os.path.dirname(__file__), 'asset', 'font.ttf'
    )
    _logger.info("Load font file: %s", font_file)
    with open(font_file, 'rb') as fp:
        file_data = fp.read()
    return file_data

_font_data = _load_font()

def get_font(size):
    return ImageFont.truetype(
        font=io.BytesIO(_font_data), size=size
    )
