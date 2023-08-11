import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SENDGRID_API_KEY  = os.environ['SENDGRID_API_KEY']

message = Mail(
    from_email='tme1@hi.is',
    to_emails='tme1@hi.is',
    subject='Sendgrid tester email',
    html_content='<strong>This is a tester email from SendGrid</strong>')
try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)