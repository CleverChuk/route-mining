from io import BytesIO
import os

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, current_app
)
import json

from werkzeug.utils import secure_filename

from lib.model import AddressEncoder
from lib.file_io import default_file_io_factory

ALLOWED_EXTENSIONS = {"xlsx", "xls"}
file_upload_blue_print = Blueprint('file_upload', __name__, url_prefix='/')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@file_upload_blue_print.route('/', methods=('GET', 'POST'))
def file_upload():
    """
        View for handling file uploads
    """
    if request.method == 'POST':
        # get json list from the request if user didn't upload a file
        addresses = request.form.get("json")
        file_io = default_file_io_factory.create(current_app.env)
        if addresses:
            filename = "user_provided.json"
            fp = BytesIO(addresses.encode('utf-8'))
            file_io.write(fp, os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))

            # redirect to report page
            return redirect(url_for('report.process_immediate', filename=filename))

        file = request.files.get('file')  # get file object from the request
        if not file or file.filename == '':
            # redirect if file is not selected or filename is empty
            return redirect(request.url)

        # validate that selected file is in ALLOWED_EXTENSIONS
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_io.write(file, os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))# store file in file system
            # redirect to report page
            return redirect(url_for('report.report', filename=filename))

    # renders file upload page
    return render_template('file_upload/file_upload.html')
