import os
import tempfile
from flask import Blueprint, jsonify, redirect, url_for, render_template, request, flash, make_response
from project import print_flush, db, app
import pdfkit
from project.utils.pdfOptions import PdfOptions

generate_bp = Blueprint('generate_bp', __name__, url_prefix='/req-pdf/')


@generate_bp.route('/pdf/', methods=['GET'])
def ping_pong():
    # query = db.engine.execute("select id from tenant_client")
    # print_flush("flush:", query.fetchone())

    # render template
    res = render_template("index.html")
    options = PdfOptions.options
    options['header-html'] = url_for('generate_bp.header_page', _external=True)
    options['header-right'] = "Microland"

    pdf = pdfkit.from_string(res, False,
                             options=options,
                             cover=url_for('generate_bp.cover_page', _external=True),
                             verbose=True)

    response = build_response(pdf, 'outputs.pdf')
    # return res
    return response


def build_response(pdf, filename):
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = (
    #     'attachment; filename=' + filename)
    response.headers['Content-Disposition'] = (
            'inline; filename=' + filename)
    return response


@generate_bp.route('/cover/', methods=['GET'])
def cover_page():
    return render_template("pages/cover-page.html")


@generate_bp.route('/header/', methods=['GET'])
def header_page():
    return render_template("layout/header.html")
