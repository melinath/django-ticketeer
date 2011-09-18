from django.conf.urls.defaults import patterns, include, url

from ticketeer.backends import backend
from ticketeer.views import TicketDetailView, TicketListView, HomeView


urlpatterns = patterns( '',
	url(r"^$", HomeView.as_view(), name="ticketeer_home"),
	url(r"^tickets/(?P<ticket_id>\d+)$", TicketDetailView.as_view(), name="ticketeer_ticket_detail"),
	url(r"^tickets$", TicketListView.as_view(), name="ticketeer_ticket_list"),
)