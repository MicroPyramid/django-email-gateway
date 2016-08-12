from django.template import loader
from django.conf import settings
import boto.ses


def sending_mail(subject, email_template_name, context, from_email, to_email):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    htmly = loader.get_template(email_template_name)
    html_content = htmly.render(context)
    conn = boto.ses.connect_to_region(
        'eu-west-1',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = conn.send_email(
        from_email, subject, html_content, [to_email], format='html')
    print (response)
