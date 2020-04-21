__author__ = 'deadblue'

import logging
logging.basicConfig(
    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(name)s - %(message)s'
)

import web

app = web.create_app()
