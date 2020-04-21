__author__ = 'deadblue'

import logging
import math
import io

from PIL import Image, ImageDraw

from logohub._font import get_font
from logohub._scheme import white, black

_logger = logging.getLogger(__name__)

class Logo:

    # texts
    _prefix = None
    _suffix = None
    _transparent = None
    # font object
    _font = None
    _scheme = None
    # text size
    _prefix_w = 0
    _suffix_w = 0
    _text_h = 0
    # other size
    _padding = 0
    _text_margin_w = 0
    _text_margin_h = 0
    _round_radius = 0

    def __init__(self, prefix:str, suffix:str,
                 font_size:int=60, scheme:str='black',
                 transparent:bool=False):
        """
        :param prefix: Prefix text.
        :param suffix: Suffix text.
        :param font_size: Font size in pixel, default is 60.
        :param scheme: Color scheme, "black" or "white", default is "black".
        :param transparent: Indicate whether background is transparent, default is false.
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
        self._measure(font_size)

    def _measure(self, font_size):
        """
        Calculate size and position for all objects on the logo.
        :return:
        """
        # Measure text size
        _, self._text_h = self._font.getsize('bg')
        self._prefix_w, _ = self._font.getsize(self._prefix)
        self._suffix_w, _ = self._font.getsize(self._suffix)
        # Calculate sizes bases on the font size
        self._padding = int(math.ceil(font_size / 3.0))
        self._text_margin_w = int(math.ceil(font_size / 10.0))
        self._text_margin_h = int(math.ceil(font_size / 10.0))
        self._round_radius = int(math.ceil(font_size / 10.0))

    def render(self):
        # Image size
        image_w = self._padding * 2 + self._text_margin_w * 4 + self._prefix_w + self._suffix_w
        image_h = self._padding * 2 + self._text_margin_h * 2 + self._text_h
        # Image mode and color
        img_mode, img_color = 'RGB', self._scheme.background_color
        if self._transparent:
            img_mode = 'RGBA'
            img_color = (img_color[0], img_color[1], img_color[2], 0)
        img = Image.new(mode=img_mode, size=(image_w, image_h), color=img_color)
        # Create draw
        draw = ImageDraw.Draw(img)
        # Draw highlight box
        draw.rectangle(
            xy=(
                self._padding + self._text_margin_w * 2 + self._prefix_w,
                self._padding + self._round_radius,
                image_w - 1 - self._padding,
                image_h - 1 - self._padding - self._round_radius

            ), fill=self._scheme.highlight_color, width=0
        )
        draw.rectangle(
            xy=(
                self._padding + self._text_margin_w * 3 + self._prefix_w,
                self._padding,
                image_w - 1 - self._padding - self._round_radius,
                image_h - 1 - self._padding

            ), fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._padding + self._text_margin_w * 2 + self._prefix_w,
                self._padding,
                self._padding + self._text_margin_w * 2 + self._prefix_w + self._round_radius * 2,
                self._padding + self._round_radius * 2
            ), start=180, end=270, fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                image_w - 1 - self._padding - self._round_radius * 2,
                self._padding,
                image_w - 1 - self._padding,
                self._padding + self._round_radius * 2
            ), start=270, end=0, fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._padding + self._text_margin_w * 2 + self._prefix_w,
                image_h - 1 - self._padding - self._round_radius * 2,
                self._padding + self._text_margin_w * 2 + self._prefix_w + self._round_radius * 2,
                image_h - 1 - self._padding
            ), start=90, end=180, fill=self._scheme.highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                image_w - 1 - self._padding - self._round_radius * 2,
                image_h - 1 - self._padding - self._round_radius * 2,
                image_w - 1 - self._padding,
                image_h - 1 - self._padding
            ), start=0, end=90, fill=self._scheme.highlight_color, width=0
        )
        # Draw texts
        draw.text(
            xy=(
                self._padding + self._text_margin_w,
                self._padding + self._text_margin_h
            ), text=self._prefix, fill=self._scheme.prefix_color, font=self._font
        )
        draw.text(
            xy=(
                self._padding + self._text_margin_w * 3 + self._prefix_w,
                self._padding + self._text_margin_h
            ), text=self._suffix, fill=self._scheme.suffix_color, font=self._font
        )
        return img

    def png(self):
        out = io.BytesIO()
        self.render().save(out, 'png')
        return out.getvalue()

    def webp(self):
        out = io.BytesIO()
        self.render().save(out, 'webp')
        return out.getvalue()
