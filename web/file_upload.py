import imp
import os

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app
)
import json

from werkzeug.utils import secure_filename

from lib.model import AddressEncoder

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
        addresses = request.form.get("json") # get json list from the request if user didn't upload a file
        if addresses:
            filename = "user_provided.json"
            with open(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename), "w") as fp:  # open file for writing
                json.dump(json.loads(addresses), fp, cls=AddressEncoder)   
            return redirect(url_for('report.process_immediate', filename=filename)) # redirect to report page

        file = request.files.get('file') # get file object from the request
        if not file or file.filename == '':
            return redirect(request.url) # redirect if file is not selected or filename is empty

        if allowed_file(file.filename): # validate that selected file is in ALLOWED_EXTENSIONS
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)) # store file in file system
            return redirect(url_for('report.report', filename=filename)) # redirect to report page



    return render_template('file_upload/file_upload.html') # renders file upload page
