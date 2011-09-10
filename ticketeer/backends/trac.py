"""
The trac backend simulates a Trac environment in order to leave as much of the work as possible with the Trac backend.

"""


from django.conf import settings
from trac.env import Environment
from trac.web.api import Request


TRAC_ENV = Environment(settings.TICKETEER_TRAC_ENV)


class TracBackend(object):
	"""
	Provides methods for returning the necessary data for a ticket search/a filtered ticket view, a ticket detail view, and an attachment (diff) view.
	
	Also provides methods for submitting, editing, and commenting on tickets.
	
	"""
	
	def _get_trac_request(self, path):
		"""Builds a Trac request which pretends to be pointed at the given path."""
		request = Request(
	
	def get_ticket(self):
		pass
	
	def get_ticket_list(self):
		pass
	
	def get_attachment(self):
		pass
