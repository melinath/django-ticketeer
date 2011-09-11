"""
The trac backend simulates a Trac environment in order to leave as much of the work as possible with the Trac backend.

"""

from django.conf import settings
from trac.env import Environment
from trac.ticket.api import TicketSystem
from trac.ticket.model import Ticket
from trac.ticket.query import Query

from ticketeer.backends.base import BaseBackend


class TracBackend(BaseBackend):
	"""
	Provides methods for returning the necessary data for a ticket search/a filtered ticket view, a ticket detail view, and an attachment (diff) view.
	
	Also provides methods for submitting, editing, and commenting on tickets.
	
	"""
	key = 'trac'
	
	def __init__(self):
		self.env = Environment(settings.TICKETEER_TRAC_ENV)
	
	def get_ticket(self, ticket_id=None):
		"""Returns a ticket from the database for the given ticket_id. The ticket should be treated like a dictionary for data access."""
		return Ticket(self.env, ticket_id, version=None)
	
	def get_ticket_list(self, cleaned_data):
		constraints = self._parse_cleaned_data(cleaned_data)
		query = self._build_query(constraints)
		return query.execute()
	
	def _parse_cleaned_data(self, cleaned_data):
		"""Given a form's cleaned_data, builds a dictionary of constraints suitable for trac."""
		clauses = []
		query_string = cleaned_data['q']
		return [{k: query_string} for k in ('cc', 'description', 'keywords', 'owner', 'reporter', 'summary') if query_string]
	
	def _build_query(self, constraints):
		"""
		Builds a :class:`trac.ticket.query.Query` object from this form's cleaned_data.
		
		"""
		query_kwargs = {
			# Query expects the following args on instantiation:
			#
			# env: The trac environment. This is the only required item.
			'env': self.env,
			# constraints: the actual filter constraints.
			'constraints': constraints,
			# cols: Fields which are displayed in the query. For now, we should
			#       just fetch all the fields, since the actual display should
			#       be controlled in the template. Those fields are:
			#           cc				Cc
			#           component		Component
			#           time			Created
			#           description		Description
			#           keywords		Keywords
			#           milestone		Milestone
			#           changetime		Modified
			#           owner			Owner
			#           priority		Priority
			#           reporter		Reporter
			#           resolution		Resolution
			#           status			Status
			#           summary			Summary
			#           id				Ticket
			#           type			Type
			#           version			Version
			#       (We actually gather all available fields dynamically.)
			'cols': [f['name'] for f in TicketSystem(self.env).get_ticket_fields()],
			# order: The field to order by.
			# desc: Whether the ordering is descending or ascending.
			#
			#
			# report: id of a cached query. Ignore.
			# rows: Can be set to display the ticket description beneath the
			#       summary. These would be added to the query, but we're
			#       already using all the fields anyway, so ignore this.
			# page, max: The page number and max number of objects. Together
			#            these are used for pagination, which should be handled
			#            by django. Therefore, we ignore this for now.
			#
			#            TODO: Set these later, during pagination in a custom
			#            paginator?
			#
			# max: The max number of objects. Is this used in the query?
			# format: Used to determine how each ticket is displayed by trac.
			#         Ignore this.
			# verbose: Same as having ``description`` in the rows. Ignore this.
			# report: the id of a corresponding saved query. We just ignore
			#         this.
			# group: Which field to group by. See the list of fields above.
			#        Ignore for now.
			# groupdesc: Whether the groups should be in reversed order. Ignore
			#            for now.
		}
		return Query(**query_kwargs)
