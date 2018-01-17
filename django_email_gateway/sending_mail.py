import boto.ses
import requests
import sendgrid
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings


def sending_mail(subject, email_template_name, context, from_email, to_email, verified):
    mfrom = settings.DEFAULT_FROM_EMAIL
    if verified:
        mail_sender = settings.MAIL_SENDER
    else:
        mail_sender = settings.INACTIVE_MAIL_SENDER
    htmly = loader.get_template(email_template_name)
    html_content = htmly.render(context)

    if mail_sender == 'AMAZON':
        conn = boto.ses.connect_to_region(
            settings.AWS_HOST_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        conn.send_email(from_email, subject, html_content, [to_email], format='html')
    elif mail_sender == 'MAILGUN':
        requests.post(
            settings.MGUN_API_URL,
            auth=('api', settings.MGUN_API_KEY),
            data={
                'from': mfrom,
                'to': [to_email],
                'subject': subject,
                'html': html_content,
            })
    elif mail_sender == 'SENDGRID':
        sg = sendgrid.SendGridClient(settings.SG_USER, settings.SG_PWD)
        sending_msg = sendgrid.Mail()
        sending_msg.set_subject(subject)
        sending_msg.set_html(html_content)
        sending_msg.set_text(subject)
        sending_msg.set_from(from_email)
        sending_msg.add_to(to_email)
        sg.send(sending_msg)
    else:
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
