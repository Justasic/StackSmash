from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from docutils.core import publish_parts
from docutils.core import publish_cmdline
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from django.core.cache import cache
from django.template import loader
import os

# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = False

# The default formatter
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)

# Add name -> formatter pairs for every variant you want to use
VARIANTS = {
     'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}

class Pygments(Directive):
    """ Source code syntax hightlighting.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        formatter = self.options and VARIANTS[self.options.keys()[0]] or DEFAULT
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

# Add syntax highlighting to code blocks
directives.register_directive('sourcecode', Pygments)
directives.register_directive('code', Pygments)

def plaintext(request, path):
    filePath = os.path.join(settings.DOC_PATH, path)
    ctx = {
        'parts': {
            "title": path,
            "html_title": path,
            "fragment": open(filePath).read().replace('\n', '<br>'),
        },
    }
    return render_to_response('docs/docs.html', RequestContext(request, ctx))


# Show the document rendered with docutils reStructuredText when the
# file suffix is .rst, otherwise print as plain text.
def page(request, path):
    key = 'ss.doc.page.%s' % (path.replace('/', '.'))
    #ctx = cache.get(key)
    ctx = False
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
            raise Http404("Path: " + filePath)

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

    return render_to_response('docs/docs.html', RequestContext(request, ctx))
