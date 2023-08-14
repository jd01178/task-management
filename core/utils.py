import base64
from datetime import datetime
from random import randint

import PIL
import pyotp
import six
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image
import io


def generate_key(minlength=20, maxlength=20, use_lower=True, use_upper=True, use_numbers=True, use_special=False):
    charset = ''
    if use_lower:
        charset += "abcdefghijklmnopqrstuvwxyz"
    if use_upper:
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers:
        charset += "123456789"
    if use_special:
        charset += "~@#$%^*()_+-={}|]["
    if minlength > maxlength:
        length = randint(maxlength, minlength)
    else:
        length = randint(minlength, maxlength)
    key = ''
    for i in range(0, length):
        key += charset[(randint(0, len(charset) - 1))]
    return key


class TimeStampModel(models.Model):
    slug = AutoSlugField(populate_from='slug_name')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']

    @staticmethod
    def slug_name():
        slug = generate_key(8, 8)
        return slug


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user['id']) + six.text_type(timestamp) + six.text_type(user['is_verified'])
        )


account_activation_token = AccountActivationTokenGenerator()


class GenerateKey:
    """
    Generates unique keys given phone_number
    """

    @staticmethod
    def unique_key_(phone_number):
        return str(phone_number) + str(datetime.date(datetime.now())) + settings.SECRET_KEY


def generate_totp_(phone_number) -> pyotp.TOTP:
    """
    helper function to generate time-based totp given phone_number
    """
    keygen = GenerateKey()
    key = base64.b32encode(keygen.unique_key_(phone_number).encode())  # Key is generated
    otp = pyotp.TOTP(key, digits=settings.OTP_LENGTH, interval=settings.EXPIRY_TIME)
    return otp


def validate_otp_token(phone_number: str, otp_token: str):
    """
    Function to validate otp token using phone_number and
    """
    totp = generate_totp_(phone_number)
    return totp.verify(otp_token)


# function for converting images to webp
def convert_to_webp(image):
    img = Image.open(image)
    img = img.convert('RGB')
    # img = img.resize((800, 800))
    width, height = img.size
    # Calculate the aspect ratio
    aspect_ratio = width / height
    # Calculate the new width and height
    # new_height = 630
    # new_width = int(new_height * aspect_ratio)
    # # Crop the image
    # img = img.resize((new_width, new_height), Image.ANTIALIAS)
    new_width = 800
    new_height = int(new_width / aspect_ratio)
    # Crop the image
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    # # Convert the image to WebP format
    output = io.BytesIO()
    img.save(output, format='webp', quality=60)
    output.seek(0)

    # Update the image field with the converted WebP image
    buffer = InMemoryUploadedFile(
        output, 'ImageField', f"{image.name.split('.')[0]}.webp",
        'image/webp', output.getbuffer().nbytes, None
    )
    return buffer
