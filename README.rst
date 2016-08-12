django-ses-gateway's documentation:
=====================================

Introduction:
=============

django-ses-gateway is used for sending mails from your verified domains and verifed domains with less cost. We can also use django-ses-gateway for receive messages and deliver them to an Amazon S3 bucket in an enctypted format, call your custom code via an AWS Lambda function, or publish notifications to Amazon SNS to process the response.


Installation Procedure
======================

1. Install django-ses-gateway using the following command::

    pip install django-ses-gateway

    		(or)

    git clone git://github.com/micropyramid/django-blog-it.git

    cd django-ses-gateway

    python setup.py install


2. After installing/cloning this, add the following details in settings file to send/receive emails notifications ::

    # AWS details

    AWS_ACCESS_KEY_ID = "Your AWS Access Key"

    AWS_SECRET_ACCESS_KEY = "Your AWS Secret Key"


Usage:
=======

1. Sending an email::

    sending_mail(subject, email_template_name, context, from_email, to_email)

2. Receiving an email::

    from django_ses_gateway.receiving_mail import sns_notification
    subject, from_mail, to_mail, hash_code, mail_content = sns_notification(request.body)

It will process the your message content, will return the email subject, from mail, to email(abc@yourdomain.com), hashcode(abc), mail content.



