import json
import os
from flask import Blueprint, jsonify, redirect, url_for, render_template, request, flash, make_response
from project import print_flush, db, app, settings
import pdfkit
import requests
from sqlalchemy.exc import SQLAlchemyError, DataError, DatabaseError

from project.utils.utils import error_response, success_response


# primary_audit_view
def primary_audit_helper(tenant_id):
    primary_audits_data = [{}]
    try:

        # Get infra of the provided tenant
        res = requests.get(settings.IAM_URL + "/infra-list", headers={
            "tenantid": request.headers.get("tenantid"),
        })
        res.raise_for_status()

        infra_id_list = [infra["INFRA_ID"] for infra in res.json()]

        app.logger.info(f"infra_id_list: {infra_id_list}")

        fetch_tenants_client = db.engine.execute(f"""SELECT * FROM public.tenants_client 
                        WHERE infra_uuid IN ('{infra_id_list[0]}') AND schema_name != 'public'""").all()

        for data in fetch_tenants_client:
            # app.logger.info(f"data: {data._asdict()}")
            primary_audits_data[0]["data"] = data._asdict()

        # convert uuid to hex
        tenanted_schema = infra_id_list[0].replace('-', '')

        # fetching the count of tenented audit
        fetch_audit_count = db.engine.execute(
            f"SELECT count(*) FROM {tenanted_schema}.tenanted_audit").first()
        app.logger.info(f"audit count: {fetch_audit_count._asdict()}")
        primary_audits_data[0]['total_audits_in_infra'] = fetch_audit_count['count']

        response = success_response(status="success", data=primary_audits_data)
        app.logger.info(f"response: {json.dumps(response)}")

        return response

    except (SQLAlchemyError, DataError, DatabaseError, Exception) as err:
        print_flush("Exception:", str(err))
    finally:
        pass


def build_response(pdf, filename):
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = (
    #     'attachment; filename=' + filename)
    response.headers['Content-Disposition'] = (
        'inline; filename=' + filename)
    return response
