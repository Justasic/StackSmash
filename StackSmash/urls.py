from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StackSmash.views.home', name='home'),
    # url(r'^StackSmash/', include('StackSmash.foo.urls')),

    # TODO: Fix index and use something... Should identify subdomains somehow..
    #url(r'^$', include('StackSmash.apps.blog.urls')),
    url(r'^docs/', include('StackSmash.apps.docs.urls')),
    url(r'^blog/', include('StackSmash.apps.blog.urls')),
    url(r'^projects/', include('StackSmash.apps.projects.urls')),
    #url(r'^projects/', include('StackSmash.apps.projects.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
