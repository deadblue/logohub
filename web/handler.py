__author__ = 'deadblue'

import logging

import flask

import logohub

_logger = logging.getLogger(__name__)

def show_help():
    url_prefix = '%s://%s' % (flask.request.scheme, flask.request.host)
    buf = [
        'Pronhub Style Logo Service',
        '',
        'Usage:',
        '    %s/<prefix>-<suffix>[-fontSize[-scheme]][.format]' % url_prefix,
        '',
        'Parameters:',
        '    prefix: Prefix text on the logo, can NOT be empty.',
        '    suffix: Suffix text on the logo, can NOT be empty.',
        '    fontSize: Font size, value starts from 30 to 200, default is 60.',
        '    scheme: Color scheme of the logo, can be "black" or "white", default is "black".',
        '    format: Logo image format, can be "png" or "webp", default is "png".',
        '',
        'Example:',
        '    %s/hello-world' % url_prefix,
        '    %s/hello-world-120' % url_prefix,
        '    %s/hello-world-120-white' % url_prefix,
        '    %s/hello-world-120-white.webp' % url_prefix,
        '    %s/hello-world.webp' % url_prefix
    ]
    resp = flask.make_response('\n'.join(buf), 200)
    resp.headers.set('Content-Type', 'text/plain')
    return resp

def draw_logo(spec:str):
    spec = _parse_spec(spec)
    if spec is None:
        # Redirect to root when error
        return flask.redirect('/')
    else:
        return _make_logo(spec)

def _parse_spec(text:str):
    # strip extension
    file_type = 'png'
    if text.endswith('.png'):
        file_type, text = 'png', text[:-4]
    elif text.endswith('.webp'):
        file_type, text = 'webp', text[:-5]
    # parse spec text
    fields = text.split('-')
    # prefix and suffix
    if len(fields) < 2:
        return None
    if len(fields[0]) == 0 or len(fields[1]) == 0:
        return None
    spec = {
        'prefix': fields[0],
        'suffix': fields[1],
        'font-size': 60,
        'scheme': 'black',
        'format': file_type
    }
    # font size
    if len(fields) > 2:
        font_size = int(fields[2], 10)
        if font_size == 0:
            font_size = 60
        elif font_size < 30:
            font_size = 30
        elif font_size > 200:
            font_size = 200
        spec['font-size'] = font_size
    # color scheme
    if len(fields) > 3:
        spec['scheme'] = fields[3]
    return spec

def _make_logo(spec:dict):
    # Create logo
    logo = logohub.Logo(
        spec['prefix'], spec['suffix'], spec['font-size'], spec['scheme']
    )
    # Export to specific format
    if spec.get('format', '') == 'webp':
        img_data = logo.webp()
        mime_type = 'image/webp'
        file_name = '%(prefix)s-%(suffix)s.webp' % spec
    else:
        img_data = logo.png()
        mime_type = 'image/png'
        file_name = '%(prefix)s-%(suffix)s.png' % spec
    # Make response
    resp = flask.make_response(img_data, 200)
    resp.headers.set('Content-Type', mime_type)
    resp.headers.set('Content-Disposition', 'inline', filename=file_name)
    resp.headers.set('Cache-Control', 'immutable')
    return resp
