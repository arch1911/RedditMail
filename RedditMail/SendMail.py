import smtplib
import RedditMail
from email.mime.text import MIMEText
from RedditMail.Login import get_info


def send_mail(message, receiver):
    """
    Function to send an email
    :param message: (String) Message to send
    :param receiver: (String) E-mail of the receiver
    :return:
    """
    logIn = get_info()

    msg = MIMEText(message, 'html')
    msg['Subject'] = "Reddit"
    msg['From'] = "RedditMail"
    msg['To'] = receiver

    mail = smtplib.SMTP(RedditMail.__smtpserver__, RedditMail.__smtp_port__)
    mail.ehlo()
    mail.starttls()
    mail.login(logIn[0], logIn[1])

    print("Attempting to send email...")
    mail.sendmail(logIn[1], receiver, msg.as_string())
    mail.close()
