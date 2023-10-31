from django.conf import settings
from djoser.signals import user_registered, user_activated
from django.dispatch import receiver
from .models import UserAccount
from django.core.mail import send_mail

admin_list = [
    settings.EMAIL_HOST_USER,
    "support@importlio.com",
    "rwchampin@gmail.com",
]
@receiver(user_registered)
def create_user_account(user, request, **kwargs):
    # send an email to the admin when a new user registers
    try:
        new_user = UserAccount.objects.get(email=user.email)
        
        # if new user is valid, send email to admin
        if new_user:
            # send email to admin
            subject = 'Importlio Admin: New User Registration'
            message = f'A New user has registered. \n\nEmail: {new_user.email}\n\nName: {new_user.first_name} {new_user.last_name}'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = admin_list
            send_mail( subject, message, email_from, recipient_list )
    except:
        # if new user is not valid throw an error and log it
        print("New user registration failed.")
        return Exception("New user registration failed.")
    

@receiver(user_activated)
def send_admin_notification(user, request, **kwargs):
    # send an email to the admin when a new user registers
    try:
        new_user = UserAccount.objects.get(email=user.email)
        
        # if new user is valid, send email to admin
        if new_user:
            # send email to admin
            subject = 'Importlio Admin: New User Activation'
            message = f'New user has activated their account.\n\nEmail: {new_user.email}\n\nName: {new_user.first_name} {new_user.last_name}'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = admin_list
            send_mail( subject, message, email_from, recipient_list )
    except:
        # if new user is not valid throw an error and log it
        print("New user activation failed.")
        return Exception("New user activation failed.")