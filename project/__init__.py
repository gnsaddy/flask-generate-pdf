import logging
import os
import time
from datetime import datetime as dt, timedelta, datetime, timezone
import colors
from flask import Flask, jsonify, request, redirect, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from project import settings


logging.basicConfig(level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s: \n%(message)s \n')


app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

db = SQLAlchemy(session_options={'autocommit': False, 'autoflush': True})
app.secret_key = settings.SECRET


# used for printing error messages
def print_flush(*args):
    print(" ********** start ********** ", flush=True)
    print(*args, flush=True)
    print(" ********** end ********** ", flush=True)


def create_app():
    app.threaded = True
    app.processes = 5

    # enable CORS
    CORS(app)

    # set up extensions
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)
    # configuration required
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
    # app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    app.config['POOL_SIZE'] = 10
    app.config['SQLALCHEMY_POOL_PRE_PING'] = True
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 280, "pool_timeout": 10, "pool_pre_ping": True}

    app.config['JSON_SORT_KEYS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SESSION_COOKIE_SECURE'] = True

    # register blueprint
    from project.views.generate import generate_bp
    app.register_blueprint(generate_bp)

    @app.after_request
    def after_request(response):
        """ Logging after every request. """

        if request.path == '/favicon.ico':
            return response
        elif request.path.startswith('/static'):
            return response

        now = time.time()
        timestamp = dt.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host.split(':', 1)[0]
        args = dict(request.args)

        log_params = [
            ('method', request.method, 'blue'),
            ('addr', request.remote_addr, 'yellow'),
            ('path', request.path, 'blue'),
            ('status', response.status, 'yellow'),
            ('content_length', response.content_length, 'yellow'),
            ('time', timestamp, 'magenta'),
            ('scheme', request.scheme, 'green'),
            ('ip', ip, 'red'),
            ('host', host, 'red'),
            ('params', args, 'blue'),
            # ('headers', dict(request.headers), 'green')
        ]

        request_id = request.headers.get('X-Request-ID')
        if request_id:
            log_params.append(('request_id', request_id, 'yellow'))

        parts = []
        for name, value, color in log_params:
            part = colors.color("{}={}".format(name, value), fg=color)
            parts.append(part)
        line = " ".join(parts)

        app.logger.info(line)

        return response

    @app.shell_context_processor
    def shell_context():
        return {'app': app, 'db': db}

    return app


@app.errorhandler(400)
def bad_request(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


@app.errorhandler(404)
def page_not_found(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


@app.errorhandler(500)
def internal_server_error(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


@app.errorhandler(405)
def method_not_allowed(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


# routes
@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
