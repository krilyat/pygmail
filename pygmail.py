#!/usr/bin/python

import smtplib
import getopt
import os
import sys

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from getpass import getpass

try:
    opts, args = getopt.getopt(sys.argv[1:], 'u:p:t:f:c:C:s:')
except getopt.GetoptError, err:
    print str(err)
    sys.exit(2)

for o, a in opts:
    if o == '-u':
        gmail_user = a
    elif o == '-p':
        gmail_pwd = a
    elif o == '-t':
        to = a
    elif o == '-f':
        enclosedFile = a
    elif o == '-c':
        corp = a
    elif o == '-C':
        corpFile = a
    elif o == '-s':
        subject = a

if "gmail_user" not in locals():
    gmail_user = raw_input("gmail user : ")

if "gmail_pwd" not in locals():
    gmail_pwd = getpass()

if "to" not in locals():
    to = raw_input("To : ")

if "subject" not in locals():
    subject = raw_input("Subject : ")

if "corpFile" not in locals() and "corp" not in locals():
    corp = raw_input("Fichier Contenant le corp du message : ")

if "enclosedFile" not in locals():
    enclosedFile = raw_input("Piece jointe (ne rien mettre si aucune) : ")


def mail(to, subject, text, attach):
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    if attach != "":
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # En theorie, on devrait utiliser mailServer.quit()
    # mais en pratique, ca se banane completement :(
    mailServer.close()

mail(to, subject, corp, enclosedFile)
