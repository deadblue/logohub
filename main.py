__author__ = 'deadblue'

import logging
logging.basicConfig(
    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(message)s'
)

import logohub

def _main():
    logo = logohub.Logo(
        font_size=60, prefix='Porn', suffix='Hub'
    )
    img = logo.render_image()
    img.show()

if __name__ == '__main__':
    _main()
