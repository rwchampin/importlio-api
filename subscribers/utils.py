# write a python fn that uses aws ses to send an email
# to a user with a token to verify their email address
# and activate their account

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

 
def send_verification_email(user, request):
    # what fields are required on the user model?
    
    
    # generate a token for the user
    token = PasswordResetTokenGenerator().make_token(user)

    # get the current site
    current_site = get_current_site(request)

    # build the email
    subject = 'Activate your Importlio account'
    message = render_to_string('subscribers/emails/verify.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    # send the email
    email = EmailMessage(subject, message, from_email, [to_email])
    email.send()