from collections import defaultdict
import imp
import json
import os
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app, jsonify, send_file
)

from werkzeug.utils import secure_filename
from lib import default_file_handler_chain, default_responder_pipeline
from lib.model import AddressBuilder
from lib.responder import ReportGeneratorResponder
import pandas as pd


ALLOWED_EXTENSIONS = {"xlsx", "xls"}

report_generator = ReportGeneratorResponder()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# create a blue print for views in this module
report_blue_print = Blueprint('report', __name__, url_prefix='/')


@report_blue_print.route('/report/<filename>', methods=('GET', 'POST'))
def report(filename):
    """
        View for processing uploaded file
    """
    # start the file handler chain to extract address from file
    err, addresses = default_file_handler_chain.handle(os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename))

    if err:
        raise err  # raise error if handle chain failed processing the file

    # add report generator responder to the pipeline and start the pipeline
    default_responder_pipeline.add_last(report_generator)
    default_responder_pipeline.respond(addresses)
    return render_template('report/report.html', filename=filename)


@report_blue_print.route('/immediate/<filename>', methods=('GET', 'POST'))
def process_immediate(filename):
    """
        View for processing JSON data
    """
    # start the file handler chain to extract address from file
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    with open(filename) as fp:
        addresses = json.load(fp)

    for idx in range(len(addresses)):
        row = addresses[idx]
        addresses[idx] = AddressBuilder()\
            .street_number(row["street_number"])\
            .street_name(row["street_name"])\
            .apt_number(row["apt_number"])\
            .city(row["city"])\
            .state(row["state"])\
            .zip(row["zip"])\
            .build()

    # add report generator responder to the pipeline and start the pipeline
    default_responder_pipeline.add_last(report_generator)
    default_responder_pipeline.respond(addresses)
    return render_template('report/report.html', filename=filename)


@report_blue_print.route('/data', methods=('GET',))
def report_data():
    """
        Api endpoint for retrieving the processed data
    """
    with open("web/files/data.json") as fp:  # open file containing the processed data
        payload = json.load(fp)
    return jsonify(payload)  # respond with data


@report_blue_print.route('/export', methods=('GET',))
def export_report():
    """
        View for handling file export
    """
    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], "data.json")) as fp:
        data = json.load(fp)

    # load report
    df0 = pd.DataFrame(data)
    df1 = pd.DataFrame(__addresses_per_route(data))
    exported_file_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], "export.xlsx")

    # write report to excel
    with pd.ExcelWriter(exported_file_path) as writer:
        df0.to_excel(writer, sheet_name="address_with_carrier_route")
        df1.to_excel(writer, sheet_name="address_per_route")

    # send report for downloading
    return send_file("files/export.xlsx", as_attachment=True, download_name="route_mining_report.xlsx")


def __addresses_per_route(data):
    """
        Post process the data to get address per route
    """
    counter = defaultdict(int)
    for datum in data:
        counter[datum["carrier_route"]] += 1

    return [{"Carrier Route": cr, "Address Count": count} for cr, count in counter.items()]
