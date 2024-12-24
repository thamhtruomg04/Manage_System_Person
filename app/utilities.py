from flask_mail import Message
from app import mail
from flask import current_app

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
