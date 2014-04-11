from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^about/', 'StackSmash.apps.blog.views.about'),
    url(r"^add_comment/(\d+)/$", "StackSmash.apps.blog.views.add_comment", name='add_comment'),
    url(r'^$', 'StackSmash.apps.blog.views.index', name='index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\-\w]+)/', 'StackSmash.apps.blog.views.post', name='post'),
    url(r"^archive/(\d+)/(\d+)/$", "StackSmash.apps.blog.views.archive", name='archive'),
    url(r"^delete_comment/(\d+)/$", "StackSmash.apps.blog.views.delete_comment", name="delete_comment1"),
    url(r"^delete_comment/(\d+)/(\d+)/$", "StackSmash.apps.blog.views.delete_comment", name="delete_comment2"),
    url(r"^captcha/(\d+)/(\d+)/$", "StackSmash.apps.blog.views.captcha_check", name="captcha"),
    url(r"^captcha/verify/(\d+)/(\d+)/$", "StackSmash.apps.blog.views.captcha_verify", name="captcha_verify"),
#    url(r'^$', 'archive', {'num_latest': 15}),
)
