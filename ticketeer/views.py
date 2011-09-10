from django.shortcuts import render
from django.conf import settings
from django.views.generic import DetailView, ListView
from ticketeer.backends import load_backend

#BACKEND = getattr(settings,"TICKETEER_BACKEND","ticketeer.backends.dummy.DummyBackend")
BACKEND = load_backend(settings.TICKETEER_BACKEND)


class TicketDetailView(DetailView):
	context_object_name = 'ticket'
	template_name = 'ticketeer/details.html'

	def get_object(self, *args, **kwargs):
		return BACKEND.get_ticket(self.request)

class TicketListView(ListView):
	context_object_name = 'ticket_list'
	template_name = 'ticketeer/list.html'

	def get_queryset(self):
		return BACKEND.get_ticket_list(self.request)
