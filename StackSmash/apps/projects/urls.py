from django.conf.urls import patterns, include, url
from StackSmash.apps.projects import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),

    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<slug>[\w\-]+)/$', views.detail),

)
