import threading

import pyotp
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from accounts.token import generate_totp_
from core.settings import EMAIL_HOST_USER

User = get_user_model()


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send(fail_silently=False)


def send_user_email_with_otp(user: User, subject: str, to_email: str, current_site, otp: pyotp.totp):
    """
    Generate the OTP verification email
    """
    message = render_to_string('email/account_activation_email.html',
                               {'user': user, 'domain': current_site.domain, 'otp': otp})
    EmailThread(subject, message, [to_email]).start()


def send_email_to_user(subject: str, to_email: list, data: dict):
    message = render_to_string('email/notification_email.html', {'data': data})
    EmailThread(subject, message, to_email).start()


def send_email_to_unverified_user(user: User) -> None:
    """
    Send email to unverified user.
    """
    subject = 'Account Activation'
    current_site = Site.objects.get_current()
    send_user_email_with_otp(user, subject, user.email, current_site, generate_totp_(user.email).now())
