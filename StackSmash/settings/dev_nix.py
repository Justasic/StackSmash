__author__ = 'justasic'

# To make your own dev file, copy this one and tell manage.py to run with
# the following option:
# ./manage.py [whatever] --settings=StackSmash.settings.dev_justasic
#
# Where dev_justasic is the python file you made.

from .dev import *

# Our settings key
SECRET_KEY = 'j3yo7knxot%4g#0(3&e_y!2efl%9f-=92x2see(86(nw!b&&ln'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/var/www/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'stacksmash',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'vizgix',
        'PASSWORD': 'letmein',
        'HOST': '54.82.122.161',             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',             # Set to empty string for default.
    }
}

# Add the Django debug toolbar
INSTALLED_APPS += ("debug_toolbar",)

# Add myself as an admin
ADMINS += (("Justin Crawford", "Justasic@gmail.com"),)