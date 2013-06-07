from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from docutils.core import publish_parts
from django.core.cache import cache
from django.template import loader
import os

def plaintext(request, path):
	filePath = os.path.join(settings.DOC_PATH, path)
	ctx = {
		'parts': {
			"title": path,
			"html_title": path,
			"fragment": open(filePath).read().replace('\n', '<br>'),
		},
	}
	return render_to_response('docs.html', RequestContext(request, ctx))


# Show the document rendered with docutils reStructuredText when the
# file suffix is .rst, otherwise print as plain text.
def page(request, path):
    key = 'wiki.doc.page.%s' % (path.replace('/', '.'))
    ctx = cache.get(key)
    if not ctx:

        filePath = os.path.join(settings.DOC_PATH, path)

        # "index" is the document representing its parent
        # directory. We canonicalize URLs here such that they
        # never include "index".
        #
	# Oops, too far, go back a dir.
        if os.path.basename(filePath) == 'index':
            return HttpResponseRedirect("..")
	# Call the index file if one exists.
        if os.path.isdir(filePath):
            filePath = os.path.join(filePath, 'index')
	# Could not resolve anything, 404.
        if not os.path.isfile(filePath):
            raise Http404("Path: " + path)

        ctx = {
            'parts': publish_parts(
                source = open(filePath).read(),
                writer_name = "html4css1",
                settings_overrides = {
                    'cloak_email_addresses': True,
                    'initial_header_level': 2,
                },
            ),
        }
        cache.set(key, ctx)

    return render_to_response('docs.html', RequestContext(request, ctx))
