#!/c/Python27/python
#coding: utf-8
__author__ = 'simon'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def mailfile():
    today=datetime.datetime.today().date().isoformat()
    sender = 'xxx@sina.com'
    receiver = 'yyy@qq.com'
    subject = 'SimonBak%s'%today
    smtpserver = 'smtp.sina.com'
    username = 'xxx'
    password = 'passwd'
    filename = 'bugs_%s.tar.gz'%today
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = receiver
    #attachements
    att = MIMEText(open('d:\\sandbox\\bak\\bugzilla\\%s'%filename, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=%s'%filename
    msgRoot.attach(att)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

def main():
    weekday = datetime.datetime.today().weekday()
    if weekday == 4:
        mailfile()

if __name__ == '__main__':
    main()