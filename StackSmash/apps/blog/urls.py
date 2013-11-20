from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', 'StackSmash.apps.blog.views.about'),
    url(r"^add_comment/(\d+)/$", "StackSmash.apps.blog.views.add_comment", name='add_comment'),
    url(r'^$', 'StackSmash.apps.blog.views.index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\-\w]+)/$', 'StackSmash.apps.blog.views.post', name='post'),
    url(r"^archive/(\d+)/(\d+)/$", "StackSmash.apps.blog.views.archive", name='archive'),
#    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'StackSmash.apps.blog.views.archives'),
#    url(r'^$', 'archive', {'num_latest': 15}),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
