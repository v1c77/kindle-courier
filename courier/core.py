# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
过年回家网速上行带宽太慢。写个脚本 方便用服务器传书。
唯一需求：传入文件地址， 直接发送文件给 kindle。
"""


import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# config
user = 'xxxxxx@gmail.com'
pwd = 'xxxxxx'
# to = 'heyuhuade_8a8d72@kindle.cn'
to = ['xxxxxxx@gmail.com']


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
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()  # optional
    server.login(user, pwd)
    server.sendmail(user, to, format_mail_text(user, to, 'book to you!',
                                               'Hello World.'))
    server.close()

