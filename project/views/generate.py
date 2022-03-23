import os

from flask import Blueprint, jsonify, redirect, url_for, render_template, request, flash, make_response
from project import print_flush, db, app
import pdfkit

generate_bp = Blueprint('generate_bp', __name__, url_prefix='/req-pdf/')


@generate_bp.route('/pdf/', methods=['GET'])
def ping_pong():
    # query = db.engine.execute("select id from users")
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'footer-center': 'PDF REPORT FOOTER',
        'header-center': 'PDF REPORT HEADER'
    }

    res = render_template("index.html")

    pdff = pdfkit.from_string(res, False, options=options)
    response = make_response(pdff)
    response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    # return res
    return response
