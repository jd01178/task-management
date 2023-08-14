import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *

sentry_sdk.init(
  dsn="https://559b3a5251c74d1cb41836524c3c641f@o4505594255638528.ingest.sentry.io/4505594257080320",
  integrations=[DjangoIntegration()],

  # Set traces_sample_rate to 1.0 to capture 100%
  # of transactions for performance monitoring.
  # We recommend adjusting this value in production.
  traces_sample_rate=1.0,

  # If you wish to associate users to errors (assuming you are using
  # django.contrib.auth) you may enable sending PII data.
  send_default_pii=True
)

ALLOWED_HOSTS = ["www.tmsystem.online", "tmsystem.online"]

# Security features
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SECURE_REFERRER_POLICY = 'same-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CONN_MAX_AGE = None
CONN_HEALTH_CHECKS = True
CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = ['https://tmsystem.online', 'https://www.tmsystem.online']

ADMINS = [('Dickson J', 'Joshuadickson4404@gmail.com'), ]
MANAGERS = [('Dickson J', 'Joshuadickson4404@gmail.com'),]

DEFAULT_ADMIN_PASSWORD = config("DEFAULT_ADMIN_PASSWORD")
DEFAULT_ADMIN_EMAIL = config("DEFAULT_ADMIN_EMAIL")
