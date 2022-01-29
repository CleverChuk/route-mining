import os
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.utils import secure_filename
from lib import default_file_handler_chain, default_responder_pipeline
from lib.responder import ReportGeneratorResponder



ALLOWED_EXTENSIONS = {"xlsx", "xls"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


report_blue_print = Blueprint('report', __name__, url_prefix='/')
@report_blue_print.route('/report/<filename>', methods=('GET', 'POST'))
def report(filename):
    addresses = default_file_handler_chain.handle(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))

    default_responder_pipeline.add_last(ReportGeneratorResponder())
    default_responder_pipeline.respond(addresses)
    return render_template('report/report.html')