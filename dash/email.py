from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(dash, msg):
    with dash.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    dash = current_app._get_current_object()
    msg = Message(dash.config['DASH_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=dash.config['DASH_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[dash, msg])
    thr.start()
    return thr