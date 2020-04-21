__author__ = 'deadblue'

import logging
import math

from PIL import Image, ImageDraw

from logohub._font import get_font

_logger = logging.getLogger(__name__)

_logo_color = (0, 0, 0, 255)
_highlight_color = (255 ,153, 0, 255)
_prefix_color = (255, 255, 255, 255)
_suffix_color = (0, 0, 0, 255)

class Logo:

    # texts
    _prefix = None
    _suffix = None
    # font object
    _font = None
    # text size
    _prefix_w = 0
    _suffix_w = 0
    _text_h = 0
    # other size
    _padding = 0
    _text_margin_w = 0
    _text_margin_h = 0
    _round_radius = 0

    def __init__(self, font_size, prefix, suffix):
        # Store texts
        self._prefix = prefix
        self._suffix = suffix
        # Load font
        self._font = get_font(size=font_size)
        # Measure sizes
        self._measure(font_size)

    def _measure(self, font_size):
        """
        Calculate size and position for all objects on the logo.
        :return:
        """
        # Measure text size
        self._prefix_w, self._text_h = self._font.getsize(self._prefix)
        self._suffix_w, _ = self._font.getsize(self._suffix)
        # Fix text height
        self._text_h += int(math.ceil(font_size / 6.0))
        # Calculate sizes bases on the font size
        self._padding = int(math.ceil(font_size / 3.0))
        self._text_margin_w = int(math.ceil(font_size / 10.0))
        self._text_margin_h = int(math.ceil(font_size / 10.0))
        self._round_radius = int(math.ceil(font_size / 10.0))

    def render_image(self):
        # Create image
        image_w = self._padding * 2 + self._text_margin_w * 4 + self._prefix_w + self._suffix_w
        image_h = self._padding * 2 + self._text_margin_h * 2 + self._text_h
        img = Image.new(mode='RGBA', size=(image_w, image_h), color=_logo_color)
        # Create draw
        draw = ImageDraw.Draw(img)
        # Draw highlight box
        draw.rectangle(
            xy=(
                self._padding + self._text_margin_w * 2 + self._prefix_w,
                self._padding + self._round_radius,
                image_w - self._padding,
                image_h - self._padding - self._round_radius

            ), fill=_highlight_color, width=0
        )
        draw.rectangle(
            xy=(
                self._padding + self._text_margin_w * 3 + self._prefix_w,
                self._padding,
                image_w - self._padding - self._round_radius,
                image_h - self._padding

            ), fill=_highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._padding + self._text_margin_w * 2 + self._prefix_w,
                self._padding,
                self._padding + self._text_margin_w * 2 + self._prefix_w + self._round_radius * 2,
                self._padding + self._round_radius * 2
            ), start=180, end=270, fill=_highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                image_w - self._padding - self._round_radius * 2,
                self._padding,
                image_w - self._padding,
                self._padding + self._round_radius * 2
            ), start=270, end=0, fill=_highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                self._padding + self._text_margin_w * 2 + self._prefix_w,
                image_h - self._padding - self._round_radius * 2,
                self._padding + self._text_margin_w * 2 + self._prefix_w + self._round_radius * 2,
                image_h - self._padding
            ), start=90, end=180, fill=_highlight_color, width=0
        )
        draw.pieslice(
            xy=(
                image_w - self._padding - self._round_radius * 2,
                image_h - self._padding - self._round_radius * 2,
                image_w - self._padding,
                image_h - self._padding
            ), start=0, end=90, fill=_highlight_color, width=0
        )
        # Draw texts
        draw.text(
            xy=(
                self._padding + self._text_margin_w,
                self._padding + self._text_margin_h
            ), text=self._prefix, fill=_prefix_color, font=self._font
        )
        draw.text(
            xy=(
                self._padding + self._text_margin_w * 3 + self._prefix_w,
                self._padding + self._text_margin_h
            ), text=self._suffix, fill=_suffix_color, font=self._font
        )
        return img
