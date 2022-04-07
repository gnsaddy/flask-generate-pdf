import json

from flask import jsonify


def error_response(status=None, data=None):
    return {
        'status': status,
        'data': data
    }


def success_response(status=None, data=None):
    return {
        'status': status,
        'data': data
    }
