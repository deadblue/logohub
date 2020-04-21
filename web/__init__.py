__author__ = 'deadblue'

import flask

from web import handler

def create_app():
    app = flask.Flask(__name__)
    app.add_url_rule(rule='/', endpoint='help', view_func=handler.show_help)
    app.add_url_rule(rule='/<spec>', endpoint='draw', view_func=handler.draw_logo)
    return app
