# -*- coding: utf-8 -*-
"""
过年回家网速上行带宽太慢。写个脚本 方便用服务器传书。
唯一需求：传入文件地址， 直接发送文件给 kindle。

courier send blockchain.mobi
courier set kindle-mail kindle-323123@kindle.cn
courier set mail-user mail-password...
"""
import smtplib
import os
import logging
from os.path import basename, expanduser
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import yaml

logger = logging.getLogger(__name__)
# config
# user = 'xxxxxx@gmail.com'
# pwd = 'xxxxxx'
# to = ['xxxxxxx@gmail.com']
CONF_RESERVED_KEYS = set(vars(dict).keys())
CONF_RESERVED_KEYS.update({'config_file_path',
                           'default_conf',
                           'get_config',
                           'set_config'})


class Config(dict):
    """
    一个存储全局配置的对象。
    """
    config_file_path = os.path.join(expanduser('~'), '.courier')
    default_conf = dict(
        user=None
    )

    def __init__(self, **kwargs):
        super(Config, self).__init__(kwargs)
        self.get_config()

    def get_config(self):
        if os.path.exists(self.config_file_path):
            conf = yaml.safe_load(open(self.config_file_path, 'r'))
        else:
            conf = self.set_config(**self.default_conf)
        super(Config, self).update(conf)
        return self

    def set_config(self, **kwargs):
        if os.path.exists(self.config_file_path):
            self.get_config()
        super(Config, self).update(kwargs)
        with open(self.config_file_path, 'w') as conf_fp:
            yaml.dump(dict(self), conf_fp, default_flow_style=False)
        return self

    def save(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as conf_fp:
                yaml.dump(dict(self), conf_fp, default_flow_style=False)

    def __getattr__(self, item):
        if item not in CONF_RESERVED_KEYS:
            return self.get(item)
        return getattr(self, item)

    def __setattr__(self, key, value):
        if key in CONF_RESERVED_KEYS:
            raise TypeError("You cannot set a reserved name as attribute")
        self.__setitem__(key, value)

    def __copy__(self):
        return self.__class__(self)

    def copy(self):
        return self.__copy__()


class MailBox:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 465
        self.session = None

    def __enter__(self):
        self.session = session = smtplib.SMTP_SSL(self.server, self.port)
        session.ehlo()
        session.login(self.email, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
            self.session = None
        return True

    def send_mail(self, send_to, subject='new book', text='', files=None):
        """
        :param send_to: email to address
        :type send_to: list
        :param subject: the email subject
        :type subject: str
        :param text: email body
        :type text: str
        :param files: multi email attachment
        :type files: list<file>
        :return: True & False
        """

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            part = MIMEApplication(
                f.read(),
                Name=basename(f.name)
            )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(
                basename(f.name)
            )
            msg.attach(part)

        self.session.sendmail(self.email, send_to, msg.as_string())


if __name__ == '__main__':
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.ehlo()  # optional
    # server.login(user, pwd)
    # server.sendmail(user, to, format_mail_text(user, to, 'book to you!',
    #                                            'Hello World.'))
    # server.close()
    os.remove(Config.config_file_path)
    print(Config.get_config())
