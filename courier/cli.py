# -*- coding: utf-8 -*-
import click
from courier.core import Config, MailBox

g_conf = Config()


@click.group(help='A command line tool to send book to kindle.')
def cli():
    """ command tool"""
    pass


@cli.command()
@click.argument('files', nargs=-1, type=click.File('rb'))
@click.option('--to', '-t', multiple=True, type=click.STRING)
def send(files, to):
    assert isinstance(to, (list, tuple))
    mail_box = MailBox(get_user(), get_password())
    receiver = to or get_receiver()
    with mail_box as box:
        box.send_mail(receiver, files=files)

    click.echo('[+] Done!', color='green')


@cli.command()
@click.option('--config', nargs=2, multiple=True, help='Overwrite config')
def set_conf(config):
    temp_conf = dict()
    for key, value in config:
        temp_conf[key] = value
    g_conf.set_config(**temp_conf)


def get_user():
    if not g_conf.user:
        g_conf.user = click.prompt('Gmail user account')
        g_conf.save()
    else:
        click.echo('[+] Using email account ....... {}'.format(g_conf.user))

    return g_conf.user


def get_password():
    return click.prompt('password', hide_input=True)


def get_receiver():
    if not g_conf.receiver:
        g_conf.receiver = click.prompt('the receiver')
        g_conf.save()
    else:
        click.echo('[+] Got receiver........: {}'.format(g_conf.receiver))
    assert isinstance(g_conf.receiver, str)
    return [g_conf.receiver]
