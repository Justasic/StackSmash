from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


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
        cache.delete('ss.lib.tag.post.%d' % self.id)  # invalidate for the template tag

    def get_cache_key(self):
        return "post.%d" % self.id

    def save(self):
        super(Post, self).save()
        self.invalidate_cache()

    def get_absolute_url(self):
        return '/blog/%04d/%02d/%s/' % (self.pub_date.year, self.pub_date.month, self.slug)

    class Admin:
        pass


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    body = models.TextField()
    listed = models.BooleanField(default=False)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))

    class Admin:
        pass

