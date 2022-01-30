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
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            session.pop("__flashes", None)
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('report.report', filename=filename))
        else:
            flash(f'Comptible file formats are {ALLOWED_EXTENSIONS}')

    return render_template('file_upload/file_upload.html')
