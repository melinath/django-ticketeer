from django.conf.urls.defaults import patterns, include, url
from ticketeer.views import TicketDetailView, TicketListView

urlpatterns = patterns( '',
	url(r"^ticket/details/(?P<id>\d+)$",TicketDetailView.as_view(),name="ticket_details"),
	url(r"^ticket/list$",TicketListView.as_view(),name="ticket_list"),
)