# -*- coding: utf-8 -*-
import os
import sysconfig
import pytest
from courier.core import MailBox, Config
from smtplib import SMTPAuthenticationError


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

    # dict test
    assert _conf['user'] == 'vici'
    assert _conf.user == 'vici'

    os.remove(fake_path)


def test_mail():
    box = MailBox('xxx@gmail.com', 'XXXXX')
    assert box.session is None
    with pytest.raises(SMTPAuthenticationError):
        with box:
            assert box.session is None

    assert box.session is None

    with pytest.raises(AssertionError):
        box.send_mail('aer@gmail.com', 'test_mail', 'hello world', None)

    with pytest.raises(AttributeError):
        box.send_mail(['aer@gmail.com', 'huhua@163.com'],
                      'test_mail',
                      'hello world')


def test_test():
    assert 1 == 1
