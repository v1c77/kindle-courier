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
from os.path import basename, expanduser
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import yaml

# config
# user = 'xxxxxx@gmail.com'
# pwd = 'xxxxxx'
# to = ['xxxxxxx@gmail.com']


class Config(dict):
    """
    一个存储全局配置的对象。
    """
    config_file_path = os.path.join(expanduser('~'), '.courier')
    default_conf = dict(
        user=None,
        password=None,
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


def format_mail_text(mail_from, mail_to, subject, body):
    """

    :param mail_from:
    :param mail_to:
    :param subject:
    :param body:
    :return:
    """
    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (mail_from, ", ".join(mail_to), subject, body)
    return email_text


def mail(send_from, send_to, subject, text, files=None, server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


if __name__ == '__main__':
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.ehlo()  # optional
    # server.login(user, pwd)
    # server.sendmail(user, to, format_mail_text(user, to, 'book to you!',
    #                                            'Hello World.'))
    # server.close()
    os.remove(Config.config_file_path)
    print(Config.get_config())
