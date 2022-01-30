from collections import defaultdict
import imp
import json
import os
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app, jsonify, send_file
)

from werkzeug.utils import secure_filename
from lib import default_file_handler_chain, default_responder_pipeline
from lib.responder import ReportGeneratorResponder
import pandas as pd



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
    return render_template('report/report.html', filename=filename)

@report_blue_print.route('/data', methods=('GET',))
def report_data():
    with open("web/files/data.json") as fp:
        payload = json.load(fp)
    return jsonify(payload)  

@report_blue_print.route('/export/<filename>', methods=('GET',))
def export_report(filename):
    with open("web/files/data.json") as fp:
        data = json.load(fp)

    df0 = pd.DataFrame(data)
    df1 = pd.DataFrame(__addresses_per_route(data))
    exported_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "export.xlsx") 
    
    with pd.ExcelWriter(exported_file_path) as writer:
        df0.to_excel(writer, sheet_name="address_with_carrier_route")
        df1.to_excel(writer, sheet_name="address_per_route")
    return send_file("files/export.xlsx", as_attachment=True, attachment_filename='')


def __addresses_per_route(data):
    counter = defaultdict(int)
    for datum in data:
        counter[datum["carrier_route"]] += 1
    
    return [{"Carrier Route": cr, "Address Count": count} for cr, count in counter.items()]