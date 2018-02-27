# -*- coding: utf-8 -*-
import sysconfig
from courier.core import format_mail_text, Config
import os


def test_format_mail_text():
    mail_from = '123@hh.com'
    mail_to = ['223@hh.com']
    subject = 'yellow book'
    body = 'save it!'
    format_mail_text(mail_from, mail_to, subject, body)


def test_config_no_conf_file():
    fake_path = '/tmp/.courier'
    fake_conf = {'user': 'huahua', 'password': 'huahua'}

    if os.path.exists(fake_path):
        os.remove(fake_path)
    Config.config_file_path = fake_path
    Config.default_conf = fake_conf
    _conf = Config()
    assert _conf.default_conf == fake_conf
    assert _conf.config_file_path == fake_path
    conf = _conf.get_config()
    assert conf == fake_conf
    assert os.path.exists(fake_path)
    fake_conf.update({'user': 'vici', 'mail_box': 'mail.126.com'})
    _conf.set_config(**fake_conf)
    assert _conf.get_config() == fake_conf
    os.remove(fake_path)


def test_test():
    print(sysconfig.get_python_version())
