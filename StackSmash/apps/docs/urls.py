from django.conf.urls import patterns, include, url
from StackSmash.apps.docs import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),

    url(r'^$', views.page, dict(path='')),
    url(r'^(?P<path>[a-zA-Z0-9_\-]+(/[a-zA-Z0-9_\-]+)*)/$', views.page),
    url(r'^(?P<path>[a-zA-Z0-9_\-]+\.txt)', views.plaintext),
    url(r'^(?P<path>[a-zA-Z0-9_\-]+\.rst)', views.page),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
