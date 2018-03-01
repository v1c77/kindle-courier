# -*- coding: utf-8 -*-
import sysconfig
from courier.core import Mail, Config
import os


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
    pass

def test_test():
    print(sysconfig.get_python_version())
