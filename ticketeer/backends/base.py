"""
Defines the base API for Ticketeer backends.

"""

from django import forms
from django.utils.translation import ugettext_lazy as _


class BaseQueryForm(forms.Form):
	q = forms.CharField(label=_("Search"), required=False)


class BaseBackend(object):
	"""
	This is the base object for :mod:`ticketeer` backends. It defines methods and attributes which are expected from any registered backend.
	
	"""
	#: This form class may be overridden to provide extended search
	#: functionality for the backend. The cleaned_data from this form is passed
	#: :meth:`get_ticket_list`.
	query_form = BaseQueryForm
	
	@property
	def key(self):
		"""The key is used to automatically build template paths for :mod:`ticketeer` backends."""
		raise NotImplementedError("Subclasses of BaseBackend must define a ``key`` attribute.")
	
	def get_ticket(self, ticket_id=None):
		"""Returns a ticket from the database for the given ticket_id. The ticket should be treated like a dictionary for data access."""
		raise NotImplementedError
	
	def get_ticket_list(self, cleaned_data):
		"""Receives cleaned_data from the form and returns a list of tickets which adhere to that data."""
		raise NotImplementedError
