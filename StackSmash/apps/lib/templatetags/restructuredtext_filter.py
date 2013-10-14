from django import template
from django.core.cache import cache
from docutils import nodes
from docutils.core import publish_parts
from docutils.parsers.rst import directives, Directive
from docutils.core import publish_cmdline, default_description
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe

register = template.Library()

class Pygments(Directive):
    """ Source code syntax hightlighting for ReST syntax."""
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'linenos': directives.flag,
        'emphasize-lines': directives.unchanged_required,
    }
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        args = {'noclasses': False}
        if 'linenos' in self.options:
            args['linenos'] = 'table'
        if 'emphasize-lines' in self.options:
            args['hl_lines'] = self.options['emphasize-lines'].split(',')
        formatter = HtmlFormatter(**args)
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

# Add syntax highlighting to code blocks
directives.register_directive('sourcecode', Pygments)
directives.register_directive('code', Pygments)

@register.filter(name='restructuredtextify', needs_autoescape=True)
def restructuredtextify(content, slug, autoescape=None):
	key = 'ss.lib.tag.%d' % slug
	parts = cache.get(key)
	if not parts:
		parts = publish_parts(
			source = content,
			writer_name = "html4css1",
			settings_overrides = {
				'cloak_email_addresses': True,
				'initial_header_level': 2,
			},
		)
		cache.set(key, parts)
	return mark_safe(parts['fragment'])
