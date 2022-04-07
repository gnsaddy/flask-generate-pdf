import os
from flask import Blueprint, jsonify, redirect, url_for, render_template, request, flash, make_response
from project import print_flush, db, app, settings
import pdfkit
from project.utils.pdfOptions import PdfOptions
from project.views.helper import build_response, primary_audit_helper
import requests

generate_bp = Blueprint('generate_bp', __name__, url_prefix='/get-pdf/')


@generate_bp.route('/primary-audit-pdf/', methods=['GET'])
def primary_audit_view():
    # accepting tenantid from header
    tenant_id = str(request.headers.get("tenantid"))

    response = primary_audit_helper(tenant_id)

    # render template
    rendered_template = render_template(
        "pages/primary-audit/primary-audit-pdf.html", response=response)

    # fetching the default options (configurations for pdfkit)
    options = PdfOptions.options
    options['header-html'] = url_for('generate_bp.header_page', _external=True)

    pdf = pdfkit.from_string(rendered_template, False,
                             options=options,
                             cover=url_for(
                                 'generate_bp.cover_page', _external=True),
                             verbose=True)

    return build_response(pdf, 'outputs.pdf')


@generate_bp.route('/cover/', methods=['GET'])
def cover_page():
    return render_template("pages/cover-page.html")


@generate_bp.route('/header/', methods=['GET'])
def header_page():
    return render_template("layout/header.html")
