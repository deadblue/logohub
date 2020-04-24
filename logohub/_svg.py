__author__ = 'deadblue'

template = '''<svg xmlns="http://www.w3.org/2000/svg" width="%(image_w)d" height="%(image_h)d">
  <style>
    text { font-family:Arial,Helvetica; font-weight:bold; font-size:%(font_size)dpx; }
    .prefix{ fill:%(prefix_color)s; }
    .suffix{ fill:%(suffix_color)s; }
  </style>
  <rect x="0" y="0" width="%(image_w)d" height="%(image_h)d" fill="%(bg_color)s" fill-opacity="%(bg_opacity)d"/>
  <rect x="%(hl_x)d" y="%(hl_y)d" width="%(hl_w)d" height="%(hl_h)d" fill="%(hl_color)s" rx="%(hl_radius)d" />
  <text x="%(prefix_x)d" y="%(text_y)d" class="prefix">%(prefix)s</text>
  <text x="%(suffix_x)d" y="%(text_y)d" class="suffix">%(suffix)s</text>
</svg>
'''

def color(c):
    return '#%02x%02x%02x' % c
