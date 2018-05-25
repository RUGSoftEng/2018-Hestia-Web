"""
Coordinates the CLI for the application.
"""
import click
import os
from app import (create_app)
PORT = int(os.environ.get("PORT", 5000))

@click.group()
def cli():
    """ Group that options for the command line interface. """
    pass

@click.command()
def run():
    """ Run the backend in production mode. """
    app = create_app('production')
    app.run(host="0.0.0.0", port=PORT)

@click.command()
def dev():
    """ Run the backend in development mode. """
    app = create_app('development')
    app.run(host="0.0.0.0", port=PORT)


cli.add_command(run)
cli.add_command(dev)

if __name__ == "__main__":
    cli()
