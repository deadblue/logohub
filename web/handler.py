__author__ = 'deadblue'

import logging

import flask

import logohub

from web._util import must_atoi
from web._mime import mime_types

_logger = logging.getLogger(__name__)

def favicon():
    return flask.send_file('static/favicon.ico', 'image/x-icon')

def show_help():
    url_prefix = '%s://%s' % (flask.request.scheme, flask.request.host)
    buf = [
        'Pronhub Style Logo Service',
        '',
        'Usage:',
        '    %s/<Prefix>-<Suffix>[-FontSize][.Format][?Parameters]' % url_prefix,
        '',
        'Components:',
        '    Prefix: Prefix text on the logo, can not be empty.',
        '    Suffix: Suffix text on the logo, can not be empty.',
        '    FontSize: Font size for prefix and suffix, in range of 30 to 200, default is 60.',
        '    Format: Image file format, supports svg/png/webp, default is "svg".',
        '    Parameters: QueryString-encoded optional parameters, see below for details.',
        '',
        'Parameters: ',
        '    scheme: Color scheme of the logo, supports black/white, default is "black".',
        '    transparent: Set background to transparent or not, default is "false".',
        '    padding: Padding size around the logo, unset or negative will use a default size.',
        '',
        'Example:',
        '    %s/hello-world' % url_prefix,
        '    %s/hello-world-90' % url_prefix,
        '    %s/hello-world.png' % url_prefix,
        '    %s/hello-world?transparent=true' % url_prefix,
        '    %s/hello-world-120.webp?scheme=white&transparent=true&padding=0' % url_prefix,
        ''
    ]
    resp = flask.make_response('\n'.join(buf), 200)
    resp.headers.set('Content-Type', 'text/plain')
    return resp

def draw_logo(spec:str):
    spec = _parse_spec(spec, flask.request.args)
    if spec is None:
        # Redirect to root when error
        return flask.redirect('/')
    else:
        return _make_logo(spec)

def _parse_spec(text:str, args):
    # Strip file format
    fmt = 'svg'
    if text.endswith('.svg'):
        fmt, text = 'svg', text[:-4]
    elif text.endswith('.png'):
        fmt, text = 'png', text[:-4]
    elif text.endswith('.webp'):
        fmt, text = 'webp', text[:-5]
    # Parse spec text
    fields = text.split('-')
    if len(fields) < 2 or len(fields[0]) == 0 or len(fields[1]) == 0:
        return None
    spec = {
        'prefix': fields[0],
        'suffix': fields[1],
        'font_size': 60,
        'format': fmt
    }
    # Parse font size.
    if len(fields) > 2:
        font_size = must_atoi(fields[2], 0)
        if font_size == 0:
            font_size = 60
        elif font_size < 30:
            font_size = 30
        elif font_size > 200:
            font_size = 200
        spec['font_size'] = font_size
    # Parse args
    spec['scheme'] = args.get('scheme', default='black')
    spec['transparent'] = args.get('transparent', default='false') == 'true'
    spec['padding'] = args.get('padding', default=-1, type=int)
    return spec

def _make_logo(spec:dict):
    _logger.debug('Logo spec: %r', spec)
    # Create logo
    logo = logohub.Logo(**spec)
    # Export to specific format
    fmt = spec.get('format', 'svg')
    if fmt == 'webp':
        img_data = logo.webp()
    elif fmt == 'png':
        img_data = logo.png()
    else:
        img_data = logo.svg()
    mime_type = mime_types[fmt]
    file_name = '%(prefix)s-%(suffix)s.%(format)s' % spec
    # Make response
    resp = flask.make_response(img_data, 200)
    resp.headers.set('Content-Type', mime_type)
    resp.headers.set('Content-Disposition', 'inline', filename=file_name)
    resp.headers.set('Cache-Control', 'public')
    return resp
