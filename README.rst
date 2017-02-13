django-ses-gateway:
=====================================

.. image:: https://readthedocs.org/projects/django-ses-gateway/badge/?version=latest
   :target: http://django-ses-gateway.readthedocs.io/en/latest/
   :alt: Documentation Status
   
.. image:: https://travis-ci.org/MicroPyramid/django-ses-gateway.svg?branch=master
   :target: https://travis-ci.org/MicroPyramid/django-ses-gateway

.. image:: https://img.shields.io/pypi/dm/django-ses-gateway.svg
    :target: https://pypi.python.org/pypi/django-ses-gateway
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/django-ses-gateway.svg
    :target: https://pypi.python.org/pypi/django-ses-gateway
    :alt: Latest Release

.. image:: https://coveralls.io/repos/github/MicroPyramid/django-ses-gateway/badge.svg?branch=master
   :target: https://coveralls.io/github/MicroPyramid/django-ses-gateway?branch=master

.. image:: https://landscape.io/github/MicroPyramid/django-ses-gateway/master/landscape.svg?style=flat
   :target: https://landscape.io/github/MicroPyramid/django-ses-gateway/master
   :alt: Code Health

.. image:: https://img.shields.io/github/license/micropyramid/django-ses-gateway.svg
    :target: https://pypi.python.org/pypi/django-ses-gateway/

Introduction:
=============

`Django ses gateway`_ is used for sending mails from your verified domains and verifed emails with less cost. We can also use django-ses-gateway for receive messages and deliver them to an Amazon S3 bucket in an enctypted format, call your custom code via an AWS Lambda function, or publish notifications to Amazon SNS to process the response.


Installation Procedure
======================

1. Install django-ses-gateway using the following command::

    pip install django-ses-gateway

    		(or)

    git clone git://github.com/micropyramid/django-ses-gateway.git

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

Visit our Django web development page `Here`_

We welcome your feedback and support, raise `github ticket`_ if you want to report a bug. Need new features? `Contact us here`_

.. _contact us here: https://micropyramid.com/contact-us/
.. _avaliable online: http://django-ses-gateway.readthedocs.io/en/latest/
.. _github ticket: https://github.com/MicroPyramid/django-ses-gateway/issues
.. _Django ses gateway: https://micropyramid.com/oss/
.. _Here: https://micropyramid.com/django-development-services/
