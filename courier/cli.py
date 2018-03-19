# -*- coding: utf-8 -*-
import click
from courier.core import Config, MailBox

g_conf = Config()


@click.group(help='A command line tool to send book to kindle.')
def cli():
    """ command tool"""
    pass


@cli.command()
@click.argument('files', nargs=-1, required=True, type=click.File('rb'))
@click.option('--to', '-t', multiple=True, type=click.STRING)
def send(files, to):
    assert isinstance(to, (list, tuple))
    mail_box = MailBox(get_user(), get_password())
    receiver = get_receiver(to)
    with mail_box as box:
        box.send_mail(receiver, files=files)

    click.echo('[+] Done!', color='green')


@cli.command()
@click.option('--config', required=True, nargs=2, multiple=True,
              help='overwrite/update config')
def set_conf(config):
    temp_conf = dict()
    for key, value in config:
        temp_conf[key] = value
    g_conf.set_config(**temp_conf)


@cli.command()
@click.option('--key', help='get default config')
def get_conf(key=None):
    if key:
        click.echo('{}: {}'.format(key, g_conf.get(key, None)))
    else:
        click.echo(g_conf)


def get_user():
    if not g_conf.user:
        g_conf.user = click.prompt('Gmail user account')
        g_conf.save()
    else:
        click.echo('[+] Using email account ....... {}'.format(g_conf.user))

    return g_conf.user


def get_password():
    return click.prompt('password', hide_input=True)


def get_receiver(receivers=None):
    """get conf.receiver or parse receiver from args."""
    if receivers:
        click.echo('[+] Got receiver........: {}'.format(', '.join(receivers)))
        return receivers

    if not g_conf.receiver:
        g_conf.receiver = click.prompt('the receiver')
        g_conf.save()
    else:
        click.echo('[+] Got receiver........: {}'.format(g_conf.receiver))
    assert isinstance(g_conf.receiver, str)
    return [g_conf.receiver]
