"""
The trac backend simulates a Trac environment in order to leave as much of the work as possible with the Trac backend.

"""

from datetime import datetime

from django.conf import settings
from trac.env import Environment
from trac.ticket.query import QueryModule, Query
from trac.util.datefmt import utc
from trac.web.api import Request


class FakeTracPermission(object):
	"""Fake object to give all permissions always."""
	def assert_permission(self, perm):
		return True
	
	def __contains__(self, item):
		return True
	
	def __call__(self, *args, **kwargs):
		return self


class FakeTracRequest(object):
	"""
	Wraps a Django HttpRequest so that it looks and acts like a Trac request.
	
	"""
	def __init__(self, request):
		self.request = request
		self.perm = FakeTracPermission()
		self.session = {}
		self.authname = None
	
	@property
	def args(self):
		return self.request.GET
	
	@property
	def arg_list(self):
		return self.request.GET.items()


class TracBackend(object):
	"""
	Provides methods for returning the necessary data for a ticket search/a filtered ticket view, a ticket detail view, and an attachment (diff) view.
	
	Also provides methods for submitting, editing, and commenting on tickets.
	
	"""
	
	def __init__(self):
		self.env = Environment(settings.TICKETEER_TRAC_ENV)
	
	def _get_trac_request(self, path):
		"""Builds a Trac request which pretends to be pointed at the given path."""
		return Request({}, lambda x: x)
		
	
	def get_ticket(self, request):
		pass
	
	def get_ticket_list(self, request):
		# Some data (which report is being used, sorting, verbosity...) is
		# pulled directly from request.GET.
		query_module = QueryModule(self.env)
		req = FakeTracRequest(request)
		constraints = query_module._get_constraints(req)
		
		qd = request.GET
		
		kwargs = {
			'cols': qd.getlist('col'),
			'rows': qd.getlist('row'),
			'constraints': constraints
		}
		
		kwargs.update(dict([
			(k, qd.get(k))
			for k in ('format', 'max', 'report', 'order', 'group', 'page')
		]))
		
		kwargs.update(dict([
			(k, k in qd) for k in 'desc', 'groupdesc', 'verbose'
		]))
		
		orig_list = None
		orig_time = datetime.now(utc)
		query = Query(self.env, **kwargs)
		tickets = query.execute()
		return tickets
	
	def get_attachment(self, request):
		pass
