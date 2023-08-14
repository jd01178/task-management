from .base import *  # noqa

CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_DOMAIN = ".jumba-finder.com"
CSRF_TRUSTED_ORIGINS = [SECURE_ROOT_URL, ]
