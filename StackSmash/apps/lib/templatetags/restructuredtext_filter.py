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

# This is our restructuredtextify tag to use in templates.
# The tag accepts an object which MUST have get_cache_key
# as a callable function!
@register.filter(name='restructuredtextify', needs_autoescape=True)
def restructuredtextify(content, slug, autoescape=None):
	key = 'ss.lib.tag.%s' % slug.get_cache_key()
	parts = cache.get(key)
	if not parts:
		parts = publish_parts(
			source = content,
			writer_name = "html4css1",
			settings_overrides = {
				'cloak_email_addresses': True,
				'initial_header_level': 2,
				'raw_enabled': True,
			},
		)
		# XXX: Hacky!!
		# Because docutils adds its own paragraph tags into shit, this
		# mess below attempts to correct new lines and <p> tags.
		# Docutils does not fix newlines of entered text in paragraph tags either
		# and therefore running this through the linebreaksbr tag in the template
		# causes spacing fuckups. This ugly and awful mess fixes those.
		parts['fragment'] = parts['fragment'].replace('\n', '<br />')
		parts['fragment'] = parts['fragment'].replace('<p></p>', '')
		parts['fragment'] = parts['fragment'].replace('<p>\n</p>', '')
		parts['fragment'] = parts['fragment'].replace('</p><br /><p>', '</p><p>')
		parts['fragment'] = parts['fragment'].replace('</p>\n<br /><p>', '</p><p>')
		parts['fragment'] = parts['fragment'].replace('</p><br />\n<p>', '</p><p>')
		parts['fragment'] = parts['fragment'].replace('</p>\n<br />\n<p>', '</p><p>')
		parts['fragment'] = parts['fragment'].replace('</p><br />', '</p>')
		parts['fragment'] = parts['fragment'].replace('<p><br />', '</p>')
		parts['fragment'] = parts['fragment'].replace('<br /><li>', '<li>')
		parts['fragment'] = parts['fragment'].replace('</li><br />', '</li>')
		parts['fragment'] = parts['fragment'].replace('</ol><br />', '</ol>')
		parts['fragment'] = parts['fragment'].replace('<br /></pre></div><br /><p>', '</pre></div><p>')
		cache.set(key, parts)
	
	return mark_safe(parts['fragment'])
