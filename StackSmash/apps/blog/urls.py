from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'StackSmash.apps.blog.views.index'),
    url(r'^(?P<slug>[\w\-]+)/$', 'StackSmash.apps.blog.views.post'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
