from django.conf.urls.defaults import patterns, include, url
from ticketeer.views import TicketDetailView, TicketListView

urlpatterns = patterns( '',
	url(r"^tickets/(?P<ticket_id>\d+)$",TicketDetailView.as_view(),name="ticket_detail"),
	url(r"^tickets$",TicketListView.as_view(),name="ticket_list"),
)