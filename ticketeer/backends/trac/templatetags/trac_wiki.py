from django import template
from trac.mimeview.api import Context
from trac.resource import Resource
from trac.wiki.formatter import format_to_html

from ticketeer.backends.trac.backend import TRAC_ENV


register = template.Library()


@register.filter
def trac_wiki(content):
	resource = Resource()
	context = Context(resource)
	context.req = None
	return format_to_html(TRAC_ENV, context, content)
