import boto3

def send_registration_email(email):
    # Initialize the AWS SES client
    ses_client = boto3.client('ses', region_name='us-west-2')  # Replace with your desired AWS region

    # Compose the email
    subject = 'Registration Confirmation'
    message = 'Thank you for registering!'
    sender_email = 'your_email@example.com'  # Replace with your verified sender email address
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
