from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', 'StackSmash.apps.blog.views.about'),
    url(r'^$', 'StackSmash.apps.blog.views.index'),
    #url(r'^(?P<slug>[\w\-]+)/$', 'StackSmash.apps.blog.views.post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\-\w]+)/$', 'StackSmash.apps.blog.views.post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'StackSmash.apps.blog.views.archives'),
#    url(r'^$', 'archive', {'num_latest': 15}),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
