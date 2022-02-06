import os
from random import random

from flask import Flask, render_template

from lib.file_io import MAX_CONTENT_LENGTH

from . import file_upload, report

def page_not_found(e):
    """
        renders 404 page
    """
    return render_template('error/404.html'), 404


def server_error(e):
    """
        renders 500 page
    """
    return render_template('error/500.html', error=f"{e}"), 500


def gate_way_time_out(e):
    """
        renders 504 page
    """
    return render_template('error/504.html', error=f"{e}"), 504


def create_app(config=None):
    """
        Application factory method. This creates and initializes the application
    """
    global fileIO
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if config:
        app.config.update(config)
    else:
        app.config['UPLOAD_FOLDER'] = "web/files"
        app.config['EXPORT_FILE'] = "files/export.xlsx"

    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.config['SECRET_KEY'] = str(hash(random()))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register blue prints
    app.register_blueprint(file_upload.file_upload_blue_print)
    app.register_blueprint(report.report_blue_print)

    # register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    app.register_error_handler(504, gate_way_time_out)

    return app
