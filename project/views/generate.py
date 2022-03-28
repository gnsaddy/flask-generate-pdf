import os
import tempfile
from flask import Blueprint, jsonify, redirect, url_for, render_template, request, flash, make_response
from project import print_flush, db, app
import pdfkit

generate_bp = Blueprint('generate_bp', __name__, url_prefix='/req-pdf/')


@generate_bp.route('/pdf/', methods=['GET'])
def ping_pong():
    # query = db.engine.execute("select id from tenant_client")
    # print_flush("flush:", query.fetchone())

    # render template
    count = 0
    res = render_template("index.html", count=count)
    options = {
        # 'page-size': 'A4',
        # 'encoding': 'utf-8'
    }

    try:
        pdff = pdfkit.from_string(res, False, options=options)
    finally:
        # os.remove(options['header-html'])
        pass
    response = build_response(pdff, 'outputs.pdf')
    # return res
    print_flush("count:", count)
    return response


def build_response(pdf, filename):
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = (
    #     'attachment; filename=' + filename)
    response.headers['Content-Disposition'] = (
            'inline; filename=' + filename)
    return response
