#!/usr/bin/env python
#
# Periodic cleanup job for blog comments.
# This will remove any abandoned comments that
# may have been posted by bots and did not get
# past the captcha.
#
# Use PYTHONPATH=<StackSmash dir to manage.py> ./db_cleanup.py
#
# Cronjob to run on the 12th hour of every day:
# * 12 * * * PYTHONPATH=/StackSmash /StackSmash/db_cleanup.py
#

import os, datetime

def clean_up():
	# Set Django settings module.
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StackSmash.settings")

	# import our blog stuff
	from StackSmash.apps.blog.models import Comment, Post
	
	# if comments are not listed and older than a week, delete them.
	Comment.objects.filter(listed=False, created__lt = datetime.datetime.now() - datetime.timedelta(days=7)).delete()

if __name__ == "__main__":
       clean_up()
