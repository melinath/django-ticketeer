"""
Defines the base API for Ticketeer backends.

"""

from django import forms
from django.utils.translation import ugettext_lazy as _


SEARCH_PLACEHOLDER = _("Search for tickets")


class BaseQueryForm(forms.Form):
	q = forms.CharField(label=SEARCH_PLACEHOLDER, required=False, widget=forms.TextInput(attrs={'type': 'search', 'placeholder': SEARCH_PLACEHOLDER}))


class BaseAddForm(forms.Form):
	summary = forms.CharField(label=_("Summary"))
	description = forms.CharField(label=_("Description"), widget=forms.Textarea)


class BaseEditForm(BaseAddForm):
	comment = forms.CharField(label=_("Comment"), widget=forms.TextInput)


class BaseBackend(object):
	"""
	This is the base object for :mod:`ticketeer` backends. It defines methods and attributes which are expected from any registered backend.
	
	"""
	#: This form class may be overridden to provide extended search
	#: functionality for the backend. The cleaned_data from this form is passed
	#: :meth:`get_ticket_list`.
	query_form = BaseQueryForm
	add_form = BaseAddForm
	edit_form = BaseEditForm
	
	@property
	def key(self):
		"""The key is used to automatically build template paths for :mod:`ticketeer` backends."""
		raise NotImplementedError("Subclasses of BaseBackend must define a ``key`` attribute.")
	
	def get_ticket(self, ticket_id=None):
		"""Returns a ticket from the database for the given ticket_id. The ticket should be treated like a dictionary for data access."""
		raise NotImplementedError
	
	def get_ticket_list(self, cleaned_data):
		"""Receives cleaned_data from a QueryForm and returns a list of tickets which adhere to that data."""
		raise NotImplementedError
	
	def add_ticket(self, request, cleaned_data):
		"""Receives a request and cleaned_data from an AddForm and saves a ticket to the backend based on that data. Returns the id of the new ticket."""
		raise NotImplementedError
	
	def edit_ticket(self, request, ticket, cleaned_data):
		"""Receives a request, a "ticket object" as returned by :meth:`.get_ticket`, and cleaned_data from an EditForm and saves the changes to the backend."""
		raise NotImplementedError
