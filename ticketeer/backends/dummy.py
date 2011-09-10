
class Ticket(object):
	"""
	A ticket mock
	"""
	id = 1
	title = "Ticket name"
	description = "Ticket Description"

class DummyBackend(object):
	"""
	Dummy backend
	"""
	
	def get_ticket(self, request):
		return Ticket()
	
	def get_ticket_list(self, request):
		return [Ticket(),Ticket()]
	
	def get_attachment(self, request):
		pass
