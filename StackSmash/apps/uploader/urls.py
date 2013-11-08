# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('StackSmash.apps.uploader.views',
    url(r'^$', 'list', name='list'),
)
