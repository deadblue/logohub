__author__ = 'deadblue'

import logging
import math
import io

from PIL import Image, ImageDraw

from logohub._font import get_font
from logohub._scheme import white, black

_logger = logging.getLogger(__name__)

class Logo:

    # prefix and suffix text
    _prefix, _suffix = None, None
    # transparent flag
    _transparent = None
    # padding size
    _padding = None
    # font object
    _font = None
    # color scheme
    _scheme = None
    # sizes
    _round_radius = 0
    # Prefix and suffix position
    _prefix_x, _prefix_y = 0, 0
    _suffix_x, _suffix_y = 0, 0
    # Image size
    _image_w, _image_h = 0, 0
    # Highlight size and position
    _hl_w, _hl_h, _hl_x, _hl_y = 0, 0, 0, 0

    def __init__(self, prefix:str, suffix:str, font_size:int=60,
                 scheme:str='black', transparent:bool=False, padding:int=None, **kwargs):
        """
        :param prefix: Prefix text on logo.
        :param suffix: Suffix text on logo
        :param font_size: Font size in pixel, default is 60.
        :param scheme: Color scheme, "black" or "white", default is "black".
        :param transparent: Transparent flag, pass true will make
            the background transparent, default is false.
        :param padding: Padding size around the logo, pass None or
            negative will use a auto-calculated size.
        """
        self._prefix = prefix
        self._suffix = suffix
        self._font = get_font(size=font_size)
        if scheme == 'white':
            self._scheme = white
        else:
            self._scheme = black
        self._transparent = transparent
        # Measure sizes
        self._measure(font_size, padding)

    def _measure(self, font_size:int, padding:int):
        """
        Calculate size and position for all objects on the logo.
        :param font_size
        :param padding
        :return:
        """
        # Measure text size
        _, text_h = self._font.getsize('bg')
        prefix_w, _ = self._font.getsize(self._prefix)
        _logger.debug('Prefix size: %d x %d', prefix_w, text_h)
        suffix_w, _ = self._font.getsize(self._suffix)
        _logger.debug('Suffix size: %d x %d', suffix_w, text_h)
        # Calculate padding size only when not set or negative
        if padding is None or padding < 0:
            padding = int(math.ceil(font_size / 3.0))
        # Calculate sizes bases on the font size
        text_margin_w = int(math.ceil(font_size / 10.0))
        text_margin_h = int(math.ceil(font_size / 10.0))
        self._round_radius = int(math.ceil(font_size / 10.0))
        # Prefix position
        self._prefix_x = padding + text_margin_w
        self._prefix_y = padding + text_margin_h
        _logger.debug('Prefix location: (%d, %d)', self._prefix_x, self._prefix_y)
        # Suffix position
        self._suffix_x = padding + prefix_w + text_margin_w * 3
        self._suffix_y = padding + text_margin_h
        _logger.debug('Suffix location: (%d, %d)', self._suffix_x, self._suffix_y)
        # Highlight position
        self._hl_x = padding + prefix_w + text_margin_w * 2
        self._hl_y = padding
        # Highlight size
        self._hl_w = text_margin_w * 2 + suffix_w
        self._hl_h = text_margin_h * 2 + text_h
        _logger.debug('Highlight location: (%d, %d), size: %d x %d', self._hl_x, self._hl_y, self._hl_w, self._hl_h)
        # Image size
        self._image_w = padding * 2 + text_margin_w * 4 + prefix_w + suffix_w
        self._image_h = padding * 2 + text_margin_h * 2 + text_h
        _logger.debug('Image size: %d x %d', self._image_w, self._image_h)

    def render(self):
        # Image mode and color
        img_mode, img_color = 'RGB', self._scheme.background_color
        if self._transparent:
            img_mode = 'RGBA'
            img_color = (img_color[0], img_color[1], img_color[2], 0)
        img = Image.new(mode=img_mode, size=(self._image_w, self._image_h), color=img_color)
        # Create draw
        draw = ImageDraw.Draw(img)
        # Draw highlight box
        draw.rectangle(
            xy=(
                self._hl_x,
                self._hl_y + self._round_radius,
                self._hl_x + self._hl_w - 1,
                self._hl_y + self._hl_h - self._round_radius - 1
            ), fill=self._scheme.highlight_color, width=0
        )
        draw.rectangle(
            xy=(
                self._hl_x + self._round_radius,
                self._hl_y,
                self._hl_x + self._hl_w - self._round_radius - 1,
                self._hl_y + self._hl_h - 1
            ), fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._hl_x,
                self._hl_y,
                self._hl_x + self._round_radius * 2,
                self._hl_y + self._round_radius * 2,
            ), start=180, end=270, fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._hl_x + self._hl_w - self._round_radius * 2 - 1,
                self._hl_y,
                self._hl_x + self._hl_w - 1,
                self._hl_y + self._round_radius * 2,
            ), start=270, end=0, fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._hl_x,
                self._hl_y + self._hl_h - self._round_radius * 2 - 1,
                self._hl_x + self._round_radius * 2,
                self._hl_y + self._hl_h - 1,
            ), start=90, end=180, fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._hl_x + self._hl_w - self._round_radius * 2 - 1,
                self._hl_y + self._hl_h - self._round_radius * 2 - 1,
                self._hl_x + self._hl_w - 1,
                self._hl_y + self._hl_h - 1,
            ), start=0, end=90, fill=self._scheme.highlight_color, width=0
        )
        # Draw texts
        draw.text(
            xy=(self._prefix_x, self._prefix_y), text=self._prefix,
            fill=self._scheme.prefix_color, font=self._font
        )
        draw.text(
            xy=(self._suffix_x, self._suffix_y), text=self._suffix,
            fill=self._scheme.suffix_color, font=self._font
        )
        return img

    def png(self):
        img, out = self.render(), io.BytesIO()
        img.save(out, 'png')
        img.close()
        return out.getvalue()

    def webp(self):
        img, out = self.render(), io.BytesIO()
        img.save(out, 'webp')
        img.close()
        return out.getvalue()
