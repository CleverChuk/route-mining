from collections import defaultdict
from io import BytesIO
import json
import os
from flask import (
    Blueprint, render_template, current_app, jsonify, send_file, session
)

from lib import default_file_handler_chain, default_responder_pipeline
from lib.file_io import default_file_io_factory
from lib.address import AddressBuilder
import pandas as pd

from web.file_upload import SESSION_KEY


ALLOWED_EXTENSIONS = {"xlsx", "xls"}


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
        current_app.config['UPLOAD_FOLDER'], session[SESSION_KEY] + filename))

    if err:
        raise err  # raise error if handle chain failed processing the file

    # add report generator responder to the pipeline and start the pipeline
    default_responder_pipeline.respond(addresses)
    return render_template('report/report.html', filename=filename)


@report_blue_print.route('/immediate/<filename>', methods=('GET', 'POST'))
def process_immediate(filename):
    """
        View for processing JSON data
    """
    # start the file handler chain to extract address from file
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], session[SESSION_KEY] + filename)
    file_io = default_file_io_factory.create(current_app.env)
    addresses = json.load(file_io.read(filename))
        

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
    default_responder_pipeline.respond(addresses)
    return render_template('report/report.html', filename=filename)


@report_blue_print.route('/data', methods=('GET',))
def report_data():
    """
        Api endpoint for retrieving the processed data
    """
    file_io = default_file_io_factory.create(current_app.env)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], session[SESSION_KEY] + "data.json")
    payload = json.load(file_io.read(path)) # read file containing the processed data
    return jsonify(payload)  # respond with data


@report_blue_print.route('/export', methods=('GET',))
def export_report():
    """
        View for handling file export
    """
    
    file_io = default_file_io_factory.create(current_app.env)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], session[SESSION_KEY] + "data.json")
    data = json.load(file_io.read(path))

    # load report
    df0 = pd.DataFrame(data)
    df1 = pd.DataFrame(__addresses_per_route(data))

    # write report to excel
    file = BytesIO()
    with pd.ExcelWriter(file) as writer:
        df0.to_excel(writer, sheet_name="address_with_carrier_route")
        df1.to_excel(writer, sheet_name="address_per_route")
    
    file.seek(0)
    # send report for downloading
    return send_file(file, as_attachment=True, download_name="route_mining_report.xlsx")


def __addresses_per_route(data):
    """
        Post process the data to get address per route
    """
    counter = defaultdict(int)
    for datum in data:
        counter[datum["carrier_route"]] += 1

    return [{"Carrier Route": cr, "Address Count": count} for cr, count in counter.items()]
