import os
import sendgrid
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from sendgrid.helpers.mail import *

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user_profile, timestamp):
        return (
            six.text_type(user_profile.id) + six.text_type(timestamp) +
            six.text_type(user_profile.verified)
        )

def send_email(user_profile):
    email_client = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('sataponn.phutrakul@aalto.fi')
    subject = 'Email Verification'
    to_email = Email(user_profile.user.email)
    print(user_profile.user.email)

    encoded_uid = urlsafe_base64_encode(force_bytes(user_profile.id))
    token_generator = TokenGenerator()
    token = token_generator.make_token(user_profile)
    html_content = render_to_string('email_content.html', {
        'username': user_profile.user.username,
        'host': settings.HOST,
        'uid': encoded_uid,
        'token': token,
    })
    content = Content('text/html', html_content)
    print(html_content)

    mail = Mail(from_email, subject, to_email, content)
    response = email_client.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)