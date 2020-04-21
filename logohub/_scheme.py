__author__ = 'deadblue'

class Scheme:

    _background_color = None
    _highlight_color = None
    _prefix_color = None
    _suffix_color = None

    def __init__(self, bg, hl, pf, sf):
        self._background_color = bg
        self._highlight_color = hl
        self._prefix_color = pf
        self._suffix_color = sf

    @property
    def background_color(self):
        return self._background_color

    @property
    def highlight_color(self):
        return self._highlight_color

    @property
    def prefix_color(self):
        return self._prefix_color

    @property
    def suffix_color(self):
        return self._suffix_color

white = Scheme(
    bg=(255, 255, 255), hl=(255, 153, 00),
    pf=(0, 0, 0), sf=(0, 0, 0)
)

black = Scheme(
    bg=(0, 0, 0), hl=(255, 153, 00),
    pf=(255, 255, 255), sf=(0, 0, 0)
)
