import base64
from datetime import datetime
import pyotp
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        token = six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        return token


account_activation_token = AccountActivationTokenGenerator()


def validate_otp_token(user_email: str, otp_token: str):
    """
    Function to validate users otp token
    """
    totp = generate_totp_(user_email)
    return totp.verify(otp_token)


class GenerateKey:
    """
    Generates unique keys given email
    """

    @staticmethod
    def unique_key_(email):
        return str(email) + str(datetime.date(datetime.now())) + settings.SECRET_KEY


def generate_totp_(email) -> pyotp.TOTP:
    """
    helper function to generate time-based totp given user email
    """
    keygen = GenerateKey()
    key = base64.b32encode(keygen.unique_key_(email).encode())  # Key is generated
    otp = pyotp.TOTP(key, digits=settings.OTP_LENGTH, interval=settings.EXPIRY_TIME)
    return otp
