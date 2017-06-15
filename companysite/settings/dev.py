from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&d&*56(ovxo6zjilno_ixu(u18luu^9+r#xb9wauj)tebf!%=^'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['192.168.0.4']

try:
    from .local import *
except ImportError:
    pass
