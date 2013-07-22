from django.conf.urls import patterns, include, url
from wiki import document_view as wiki

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^docs/$', wiki.page, dict(path='')),
    url(r'^docs/(?P<path>[a-zA-Z0-9_\-]+(/[a-zA-Z0-9_\-]+)*)/$', wiki.page),
    url(r'^docs/(?P<path>[a-zA-Z0-9_\-]+\.txt)', wiki.plaintext),
    url(r'^docs/(?P<path>[a-zA-Z0-9_\-]+\.rst)', wiki.page),
    #url(r'^(?P<path>[a-zA-Z0-9_\-]+', wiki.page),
)
