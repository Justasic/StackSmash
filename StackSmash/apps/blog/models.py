from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from docutils.core import publish_doctree, Publisher
from docutils.readers import doctree
from docutils.io import DocTreeInput, StringOutput

class Post(models.Model):
	slug = models.SlugField('slug', unique_for_date='pub_date', prepopulate_from=['title'], db_index=True)
	pub_date = models.DateTimeField(db_index=True)
	posted_by = models.ForeignKey(User)
	listed = models.BooleanField('Listed to public?', default=False)
	title = models.CharField(maxlength=100)
	content = models.TextField()

	def render(self):
		key = 'ss.apps.blog.%d' & self.id
		parts = cache.get(key)
		if not parts:
			document = publish_doctree(source = self.content)
			

			reader = doctree.Reader(parser_name='null')
			pub = Publisher(reader, None, None, source = DocTreeInput(document), destination_class = StringOutput)
			pub_set_writer('html4css1')
			pub.process_programmatic_settings(None, { 'cloak_email_addresses' : True, 'initial_header_level': 2 }, None)
			pub.publish()
			parts = pub.writer.parts

			cache.set(key, parts)
		return parts;


	class Admin:
		pass
