import smtplib
import RedditMail
from email.mime.text import MIMEText
from RedditMail.Login import getInfo
'''
This Function sends a message to an email
'''


def send_mail(message, receiver): # def sendMail(content, receiver)
    logIn = getInfo()

    msg = MIMEText(message, 'html')
    msg['Subject'] = "Reddit"
    msg['From'] = "[MAIL NAME]"
    msg['To'] = receiver

    mail = smtplib.SMTP(RedditMail.__smtpserver__, RedditMail.__smtp_port__)
    mail.ehlo()
    mail.starttls()
    mail.login(logIn[0], logIn[1])

    print("Attempting to send email...")
    mail.sendmail(logIn[1], receiver, msg.as_string())
    mail.close()
    print("Email sent")
