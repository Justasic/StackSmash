from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Just redirect / to /blog for now until I can
# come up with something to put on the homepage..
def to_blog(request):
    return redirect('/blog/', permanent=False)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),

    # TODO: Fix index and use something... Should identify subdomains somehow..
    #url(r'^$', include('StackSmash.apps.blog.urls')),
    url(r'^docs/', include('StackSmash.apps.docs.urls')),
    url(r'^blog/', include('StackSmash.apps.blog.urls')),
    url(r'^projects/', include('StackSmash.apps.projects.urls')),
    url(r'^upload/', include('StackSmash.apps.uploader.urls')),
    url(r'^$', to_blog),
    #url(r'^projects/', include('StackSmash.apps.projects.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
