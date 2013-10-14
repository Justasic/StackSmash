from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from docutils.core import publish_doctree, Publisher
from docutils.readers import doctree
from docutils.io import DocTreeInput, StringOutput
from docutils import nodes


class Project(models.Model):
	# Name of the project
	name = models.CharField(max_length=256)
	# the obligatory slug field
	slug = models.SlugField('Slug', unique_for_date='start_date')
	# The start date of the project
	start_date = models.DateTimeField(db_index=True)
	# The project status
	# 0 = started
	# 1 = suspended
	# 2 = abandoned
	# 3 = completed - date
	# 4 = ownership transfer
	status = models.PositiveSmallIntegerField('Status', default=0, choices=((0, 'started'),
										(1, 'suspended'),
										(2, 'abandoned'),
										(3, 'completed'),
										(4, 'ownership transfer'),))
	# The end date of the project (if applicable)
	completion_date = models.DateTimeField(null=True, blank=True)
	# Description of the project
	description = models.CharField(max_length=255)
	# The actual content on the project
	content = models.TextField()
	
	def get_absolute_url(self):
		return '/projects/%s/' % self.slug
	
	def invalidate_cache(self):
		cache.delete('ss.lib.tag.%d' % self.id) # invalidate for the template tag
		
	def get_cache_key(self):
		return "project.%d" % self.id
		
	def save(self):
		super(Project, self).save()
		self.invalidate_cache()
	
	class Admin:
		pass
