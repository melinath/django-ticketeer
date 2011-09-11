from django.shortcuts import render
from django.conf import settings
from django.views.generic import DetailView, ListView
from ticketeer.backends import load_backend

#BACKEND = getattr(settings,"TICKETEER_BACKEND","ticketeer.backends.dummy.DummyBackend")
BACKEND = load_backend(settings.TICKETEER_BACKEND)


class TicketDetailView(DetailView):
	context_object_name = 'ticket'

	def get_object(self):
		return BACKEND.get_ticket(self.kwargs['ticket_id'])
	
	def get_template_names(self):
		templates = [
			'ticketeer/tickets/%s/detail.html' % BACKEND.key,
			'ticketeer/tickets/detail.html'
		]
		if self.template_name is not None:
			templates.insert(0, self.template_name)
		return templates


class TicketListView(ListView):
	context_object_name = 'ticket_list'

	def get_queryset(self):
		form = BACKEND.query_form(self.request.GET)
		form.full_clean()
		return BACKEND.get_ticket_list(form.cleaned_data)
	
	def get_template_names(self):
		templates = [
			'ticketeer/tickets/%s/list.html' % BACKEND.key,
			'ticketeer/tickets/list.html'
		]
		if self.template_name is not None:
			templates.insert(0, self.template_name)
		return templates
