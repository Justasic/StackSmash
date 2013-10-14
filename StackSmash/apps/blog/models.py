from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from docutils.core import publish_doctree, Publisher
from docutils.readers import doctree
from docutils.io import DocTreeInput, StringOutput
from docutils import nodes
import sys

class Post(models.Model):
	pub_date = models.DateTimeField(db_index=True)
	posted_by = models.ForeignKey(User)
	listed = models.BooleanField('Listed to public?', default=False)
	slug = models.SlugField('slug', unique_for_date='pub_date', db_index=True)
	title = models.CharField(max_length=100)
	content = models.TextField()

	def __unicode__(self):
		return self.title

	def invalidate_cache(self):
		cache.delete('ss.apps.blog.%d' % self.id)
		cache.delete('ss.lib.tag.%d' % self.id) # invalidate for the template tag
		
	def save(self):
		super(Post, self).save()
		self.invalidate_cache()

	#@models.permalink
	def get_absolute_url(self):
		return '/blog/%04d/%02d/%s/' % (self.pub_date.year, self.pub_date.month, self.slug)

	def render(self):
		key = 'ss.apps.blog.%d' % self.id
		parts = cache.get(key)
		if not parts:

			# Convert the reST markup to a document tree
			document = publish_doctree(source = self.content)

			#
			# Publish that document tree as HTML. We can't use any of
			# the simpler methods in docutils.core, since we need
			# access to writer.parts
			#
			reader = doctree.Reader(parser_name='null')
			pub = Publisher(reader, None, None,
				    source = DocTreeInput(document),
				    destination_class = StringOutput)
			pub.set_writer('html4css1')
			pub.process_programmatic_settings(None, {
				'cloak_email_addresses': True,
				'initial_header_level': 2,
			}, None)

			pub.publish()
			parts = pub.writer.parts
			parts['post'] = self

			cache.set(key, parts)
		return parts


	class Admin:
		pass
