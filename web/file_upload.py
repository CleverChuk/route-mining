import os

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.utils import secure_filename

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
        file = request.files['file'] # get file object from the request
        if not file or file.filename == '':
            return redirect(request.url) # redirect if file is not selected or filename is empty

        if allowed_file(file.filename): # validate that selected file is in ALLOWED_EXTENSIONS
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)) # store file in file system
            return redirect(url_for('report.report', filename=filename)) # redirect to report page

    return render_template('file_upload/file_upload.html') # renders file upload page
