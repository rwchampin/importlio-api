import boto3
from django.conf import settings
def send_registration_email(email):
    # Initialize the AWS SES client
    ses_client = boto3.client('ses', region_name=settings.AWS_REGION_NAME)  # Replace with your desired AWS region

    # Compose the email
    subject = 'Registration Confirmation'
    message = 'Thank you for registering!'
    sender_email = settings.AWS_SES_FROM_EMAIL  # Replace with your verified sender email address
    recipient_email = email

    # Send the email
    response = ses_client.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': message}}
        }
    )

    # Check the response status
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Registration email sent successfully')
    else:
        print('Failed to send registration email')
