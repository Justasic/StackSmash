from django.conf.urls import patterns, include, url
from StackSmash.apps.projects import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>[\w\-]+)/$', views.detail),
)
