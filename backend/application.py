"""
Coordinates the running of the Hestia web backend.
"""
import click
import pytest
from flask import Flask
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix
from api import API

APP = Flask(__name__)
CORS(APP)
APP.wsgi_app = ProxyFix(APP.wsgi_app)
API.init_app(APP)


@click.group()
def cli():
    """
    Group that options for the command line interface.
    """
    pass


@click.command()
def run():
    """
    Run the backend in production mode.
    """
    APP.run(host="0.0.0.0", port=5000)


@click.command()
def dev():
    """
    Run the backend in development mode.
    """
    APP.run(host="0.0.0.0", port=5000, debug=True)

@click.command()
def test():
    """
    Run the tests.
    """
    pytest.main(["-s", "tests/"])

@click.command()
@click.option('--dbtype',
              prompt='Database type',
              default="postgresql",
              help='The type of database to initialize.')
def initdb(dbtype):
    """
    Initialize a database.
    """
    print("Initializing the " + dbtype + " database.")


cli.add_command(run)
cli.add_command(dev)
cli.add_command(initdb)
cli.add_command(test)

if __name__ == "__main__":
    cli()
