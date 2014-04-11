from django.conf.urls import patterns, include, url
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Just redirect / to /blog for now until I can
# come up with something to put on the homepage..
def to_blog(request):
    return redirect('/blog/', permanent=False)


# Follow the BSD license and allow the source/binary to reproduce
# the license and copyright message
def sslicense(request):
    slicense = """
     Copyright (c) 2012-2013 Justin Crawford <Justasic@gmail.com>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE
    """
    ctx = {
        'parts': {
            "title": "License",
            "html_title": "License",
            "fragment": slicense.replace('\n', '<br>'),
        },
    }
    return render_to_response('docs/docs.html', RequestContext(request, ctx))


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),

    # TODO: Fix index and use something... Should identify subdomains somehow..
    #url(r'^$', include('StackSmash.apps.blog.urls')),
    url(r'^license/', sslicense, name='license'),
    #url(r'^docs/', include('StackSmash.apps.docs.urls'), name='docs', app_name='docs'),
    url(r'^blog/', include('StackSmash.apps.blog.urls', namespace='blog')),
    url(r'^projects/', include('StackSmash.apps.projects.urls', namespace='projects')),
    url(r'^upload/', include('StackSmash.apps.uploader.urls', namespace='upload')),
    url(r'^$', to_blog, name='index'),

    #url(r'^projects/', include('StackSmash.apps.projects.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls), name='admin'),
)
