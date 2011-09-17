from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

from ticketeer.views import TicketDetailView, TicketListView


urlpatterns = patterns( '',
	url(r"^$", TemplateView.as_view(template_name="ticketeer/home.html"), name="ticketeer_home"),
	url(r"^tickets/(?P<ticket_id>\d+)$", TicketDetailView.as_view(), name="ticketeer_ticket_detail"),
	url(r"^tickets$", TicketListView.as_view(), name="ticketeer_ticket_list"),
)