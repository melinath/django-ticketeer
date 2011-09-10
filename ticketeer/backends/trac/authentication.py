from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from trac.web.auth import BasicAuthentication


#: This is used as the password for synced Trac users.
FAKE_PASSWORD = "!TRAC!"


class TracAuthBackend(ModelBackend):
	"""
	Authenticates users with Trac's BasicAuthentication. This requires the :setting:`TICKETEER_TRAC_HTPASSWD_PATH` setting.
	
	If a user exists in Trac but not in django, the user will be created. If a trac-generated user exists in Django but not in trac, the user will be deleted.
	
	"""
	def get_trac_auth(self):
		filename = settings.TICKETEER_TRAC_HTPASSWD_PATH
		return BasicAuthentication(filename, None)
	
	def authenticate(self, username=None, password=None):
		if username is None or password is None:
			return
		auth = self.get_trac_auth()
		
		if auth.test(username, password):
			try:
				user = User.objects.get(username=username)
			except User.DoesNotExist:
				user = User.objects.create(username=username, password=FAKE_PASSWORD)
			return user
		else:
			if username not in auth.hash:
				try:
					user = User.objects.get(username=username)
				except User.DoesNotExist:
					pass
				else:
					if user.password == FAKE_PASSWORD:
						user.delete()
			return None