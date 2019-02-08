import os
# import sendgrid
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.mail import send_mail
# from sendgrid.helpers.mail import *

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.userprofile.verified)
        )

def send_email(user_profile):
    # email_client = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    sender = 'no-reply@srfgamestore.com'
    subject = 'Email Verification'
    recipient = user_profile.user.email

    encoded_uid = urlsafe_base64_encode(force_bytes(user_profile.id)).decode()
    token_generator = TokenGenerator()
    token = token_generator.make_token(user_profile.user)
    html_content = render_to_string('email_content.html', {
        'username': user_profile.user.username,
        'host': settings.HOST,
        'uid': encoded_uid,
        'token': token,
    })
    # print(html_content)

    # mail = Mail(Email(sender), subject, Email(recipient), Content('text/html', html_content))
    # response = email_client.client.mail.send.post(request_body=mail.get())

    # print(response.status_code)
    # print(response.body)

    send_mail(subject, html_content, sender, [recipient])

def decode_base64(decoded):
    return force_text(urlsafe_base64_decode(decoded))

def validate_token(user, token):
    token_generator = TokenGenerator()
    return token_generator.check_token(user, token)