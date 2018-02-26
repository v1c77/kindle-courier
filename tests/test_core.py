# -*- coding: utf-8 -*-
import sysconfig
from courier.core import format_mail_text


def test_format_mail_text():
    mail_from = '123@hh.com'
    mail_to = ['223@hh.com']
    subject = 'yellow book'
    body = 'save it!'
    format_mail_text(mail_from, mail_to, subject, body)


def test_test():
    print(sysconfig.get_python_version())
