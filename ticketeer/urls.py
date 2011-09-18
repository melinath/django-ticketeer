from django.conf.urls.defaults import patterns, include, url

from ticketeer.backends import backend
from ticketeer.views import TicketDetailView, TicketListView, HomeView, TicketCreateView


urlpatterns = patterns( '',
	url(r"^$", HomeView.as_view(), name="ticketeer_home"),
	url(r"^tickets/(?P<ticket_id>\d+)$", TicketDetailView.as_view(), name="ticketeer_ticket_detail"),
	url(r"^tickets$", TicketListView.as_view(), name="ticketeer_ticket_list"),
	url(r"^tickets/new$", TicketCreateView.as_view(), name="ticketeer_new_ticket")
)