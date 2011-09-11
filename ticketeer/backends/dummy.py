from ticketeer.backends.base import BaseBackend


class Ticket(object):
	"""
	A ticket mock
	"""
	def __init__(self, id=1, name="Ticket Name", description="Ticket Description"):
		self.id = id
		self.name = name
		self.description = description

class DummyBackend(BaseBackend):
	"""
	Dummy backend
	"""
	
	def get_ticket(self, request):
		return Ticket()
	
	def get_ticket_list(self, request):
		return [Ticket(1),Ticket(2)]
