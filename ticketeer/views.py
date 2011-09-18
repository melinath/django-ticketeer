from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from ticketeer.backends import backend


class HomeView(TemplateView):
	template_name = "ticketeer/home.html"
	
	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['form'] = backend.query_form()
		return context


class TicketListView(ListView):
	context_object_name = 'ticket_list'

	def get_queryset(self):
		self.form = backend.query_form(self.request.GET)
		self.form.full_clean()
		return backend.get_ticket_list(self.form.cleaned_data)
	
	def get_template_names(self):
		templates = [
			'ticketeer/tickets/%s/list.html' % backend.key,
			'ticketeer/tickets/list.html'
		]
		if self.template_name is not None:
			templates.insert(0, self.template_name)
		return templates
	
	def get_context_data(self, **kwargs):
		context = super(TicketListView, self).get_context_data(**kwargs)
		context['form'] = self.form
		return context


class TicketDetailView(FormView, DetailView):
	context_object_name = 'ticket'
	
	def get_form_class(self):
		return backend.edit_form
	
	def get_object(self):
		return backend.get_ticket(self.kwargs['ticket_id'])
	
	def get_template_names(self):
		templates = [
			'ticketeer/tickets/%s/detail.html' % backend.key,
			'ticketeer/tickets/detail.html'
		]
		if self.template_name is not None:
			templates.insert(0, self.template_name)
		return templates
	
	def form_valid(self, form):
		backend.edit_ticket(self.request, self.get_object(), form.cleaned_data)
		return super(TicketDetailView, self).form_valid(form)
	
	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		context = DetailView.get_context_data(self, object=self.object, **kwargs)
		
		try:
			context['ticket_changes'] = backend.get_ticket_changes(self.object)
		except NotImplementedError:
			pass
		
		return context
	
	def get_success_url(self):
		return reverse("ticketeer_ticket_detail", kwargs={'ticket_id': self.kwargs['ticket_id']})


class TicketCreateView(FormView):
	def get_form_class(self):
		return backend.add_form
	
	def get_template_names(self):
		templates = [
			'ticketeer/tickets/%s/new.html' % backend.key,
			'ticketeer/tickets/new.html'
		]
		if self.template_name is not None:
			templates.insert(0, self.template_name)
		return templates
	
	def form_valid(self, form):
		self.ticket_id = backend.add_ticket(self.request, form.cleaned_data)
		return super(TicketCreateView, self).form_valid(form)
	
	def get_success_url(self):
		return reverse("ticketeer_ticket_detail", kwargs={'ticket_id': self.ticket_id})
