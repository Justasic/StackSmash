#!/usr/bin/env python
#
# Periodic cleanup job for blog comments.
# This will remove any abandoned comments that
# may have been posted by bots and did not get
# past the captcha.
#
# Use PYTHONPATH=<StackSmash dir to manage.py> ./db_cleanup.py
#

import os, datetime

def clean_up():
	# Set Django settings module.
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StackSmash.settings")

	# import our blog stuff
	from StackSmash.apps.blog.models import Comment, Post
	comments = Comment.objects.filter(listed=False).order_by("created")
	
	# If comments are older than a day, delete them.
	for comment in comments:
		if comment.created.day < datetime.datetime.now().day:
			Comment.objects.filter(listed=False, id=comment.id).delete()


if __name__ == "__main__":
	clean_up()
