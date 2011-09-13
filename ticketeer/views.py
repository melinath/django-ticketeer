from django.shortcuts import render
from django.conf import settings
from django.views.generic import DetailView, ListView
from django.views.generic.edit import ProcessFormView, FormMixin
from ticketeer.backends import load_backend

#BACKEND = getattr(settings,"TICKETEER_BACKEND","ticketeer.backends.dummy.DummyBackend")
BACKEND = load_backend(settings.TICKETEER_BACKEND)


class TicketAddView(ProcessFormView, FormMixin):
	def get_form_class(self):
		return BACKEND.add_form
	
	def get_template_names(self):
		templates = [
			'ticketeer/tickets/%s/add.html' % BACKEND.key,
			'ticketeer/tickets/add.html'
		]
		if self.template_name is not None:
			templates.insert(0, self.template_name)
		return templates
	
	def form_valid(self, form):
		BACKEND.add_ticket(form.cleaned_data)
		return super(TicketAddView, self).form_valid(form)


class TicketDetailView(ProcessFormView, FormMixin, DetailView):
	context_object_name = 'ticket'
	
	def get_form_class(self):
		return BACKEND.edit_form
	
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
	
	def form_valid(self, form):
		BACKEND.edit_ticket(form.cleaned_data)
		return super(TicketDetailView, self).form_valid(form)
	
	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		return DetailView.get_context_data(self, object=self.object, **kwargs)


class TicketListView(ListView):
	context_object_name = 'ticket_list'

	def get_queryset(self):
		self.form = BACKEND.query_form(self.request.GET)
		self.form.full_clean()
		return BACKEND.get_ticket_list(self.form.cleaned_data)
	
	def get_template_names(self):
		templates = [
			'ticketeer/tickets/%s/list.html' % BACKEND.key,
			'ticketeer/tickets/list.html'
		]
		if self.template_name is not None:
			templates.insert(0, self.template_name)
		return templates
	
	def get_context_data(self, **kwargs):
		context = super(TicketListView, self).get_context_data(**kwargs)
		context['form'] = self.form
		return context
