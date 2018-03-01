# -*- coding: utf-8 -*-
import click
from courier.core import Config

_g_conf = Config()


@click.group(help='A command line tool to send book to kindle.')
def cli():
    """do something..."""
    pass


@cli.command()
def send():
    click.echo('send books.')


@cli.command()
def set_conf():
    click.echo('set conf')
