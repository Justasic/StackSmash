__author__ = 'justasic'

from .base import *

ADMINS += (
    # ('Your Name', 'your_email@example.com'),
      ('Justin Crawford', 'Justasic@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'stacksmash',            # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',             # Set to empty string for default.
    }
}

SITE_ID = 1

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/var/www/media/'