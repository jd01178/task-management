# To hold utility functions

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from accounts.email import send_user_email_with_otp
from accounts.token import generate_totp_

User = get_user_model()


def send_email_to_unverified_user_(user: User) -> None:
    """
    Send email to unverified user.
    """
    subject = 'Account Activation'
    current_site = Site.objects.get_current()
    send_user_email_with_otp(user, subject, user.email, current_site, generate_totp_(user.email).now())
