"""
Coordinates the CLI for the application.
"""
import click
from app import (create_app)

@click.group()
def cli():
    """ Group that options for the command line interface. """
    pass

@click.command()
def run():
    """ Run the backend in production mode. """
    app = create_app('production')
    app.run(host="0.0.0.0")

@click.command()
def dev():
    """ Run the backend in development mode. """
    app = create_app('development')
    app.run(host="0.0.0.0")

cli.add_command(run)
cli.add_command(dev)

if __name__ == "__main__":
    cli()
