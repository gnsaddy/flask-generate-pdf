import unittest
from flask.cli import FlaskGroup
from project import db, create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)


if __name__ == '__main__':
    cli()
    # app.run()