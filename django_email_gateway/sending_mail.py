import base64

import requests
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings
import boto3
from botocore.exceptions import ClientError


def sending_mail(subject, email_template_name, context, from_email, to_email, verified, cc_list=None, bcc_list=None):
    """
    :param subject: string
    :param email_template_name: string
    :param context: string
    :param from_email: mail id
    :param to_email: mail id or list of mail ids
    :param verified: string
    :param cc_list: mail id or list of mail ids
    :param bcc_list: mail id or list of mail ids
    :return:
    """
    mfrom = settings.DEFAULT_FROM_EMAIL
    if verified:
        mail_sender = settings.MAIL_SENDER
    else:
        mail_sender = settings.INACTIVE_MAIL_SENDER
    htmly = loader.get_template(email_template_name)
    html_content = htmly.render(context)
    recipients = [to_email]
    if isinstance(to_email, list):
        recipients = to_email
    ccs = list()
    if cc_list:
        ccs = [cc_list]
        if isinstance(cc_list, list):
            ccs = cc_list
    bccs = list()
    if bcc_list:
        bccs = [bcc_list]
        if isinstance(bcc_list, list):
            bccs = bcc_list

    if mail_sender == 'AMAZON':
        client = boto3.client('ses',
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                              )
        recipients = [to_email]
        if isinstance(to_email, list):
            recipients = to_email
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': recipients,
                    'CcAddresses': ccs,
                    'BccAddresses': bccs
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': htmly,
                        }
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=from_email,
            )
            return {'message': 'Mail sent', 'data': response['ResponseMetadata']['RequestId']}
        except ClientError as e:
            raise e.response['Error']['Message']
    elif mail_sender == 'MAILGUN':
        try:
            response = requests.post(
                settings.MGUN_API_URL,
                auth=('api', settings.MGUN_API_KEY),
                data={
                    'from': mfrom,
                    'to': recipients,
                    'subject': subject,
                    "cc": ccs,
                    "bcc": bccs,
                    'html': html_content,
                })
            return {'message': 'Mail sent', 'data': response.json()}
        except Exception:
            raise Exception

    elif mail_sender == 'SENDGRID':
        import sendgrid
        sg = sendgrid.SendGridClient(settings.SG_USER, settings.SG_PWD)
        sending_msg = sendgrid.Mail()
        if bcc_list:
            if isinstance(bcc_list, list):
                for bcc_mail in bcc_list:
                    sending_msg.add_bcc(bcc_email=bcc_mail)
            else:
                sending_msg.add_bcc(bcc_email=bcc_list)
        if cc_list:
            if isinstance(cc_list, list):
                for cc_mail in cc_list:
                    sending_msg.add_cc(cc_email=cc_mail)
            else:
                sending_msg.add_cc(cc_email=cc_list)
        sending_msg.set_subject(subject)
        sending_msg.set_html(html_content)
        sending_msg.set_text(subject)
        sending_msg.set_from(from_email)
        sending_msg.add_to(to_email)
        try:
            response = sg.send(sending_msg)
            return {'message': 'Mail sent', 'data': response}
        except Exception:
            raise Exception
    elif mail_sender == 'MAILJET':
        from mailjet_rest import Client
        API_KEY = settings.MJ_APIKEY_PUBLIC
        API_SECRET = settings.MJ_APIKEY_PRIVATE
        mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')
        to_list = list()
        for recipient in recipients:
            to_list.append({
                "Email": recipient,
                "Name": ''.join(recipient.split('@')[0].split('.'))
            })
        ccs_list = list()
        for recipient in ccs:
            ccs_list.append({
                "Email": recipient,
                "Name": ''.join(recipient.split('@')[0].split('.'))
            })
        bccs_list = list()
        for recipient in bccs:
            bccs_list.append({
                "Email": recipient,
                "Name": ''.join(recipient.split('@')[0].split('.'))
            })
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": from_email,
                        "Name": "Me"
                    },
                    "To": to_list,
                    "Cc": ccs_list,
                    'Bcc': bccs_list,
                    "Subject": subject,
                    "HTMLPart": html_content
                }
            ]
        }
        try:
            result = mailjet.send.create(data=data)
            return {'message': 'Mail sent', 'data': result.json()}
        except Exception:
            raise Exception
    else:
        msg = EmailMultiAlternatives(subject, html_content, from_email, recipients, cc=ccs, bcc=bccs)
        msg.attach_alternative(html_content, "text/html")
        try:
            response = msg.send()
            return {'message': 'Mail sent', 'data': response}
        except Exception:
            raise Exception
