import smtplib

server = smtplib.SMTP('' , 25)

server.ehlo()
