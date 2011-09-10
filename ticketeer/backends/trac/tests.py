from __future__ import with_statement
import os

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import unittest
from trac.web.auth import BasicAuthentication

from ticketeer.backends.trac.authentication import TracAuthBackend, FAKE_PASSWORD
from ticketeer.backends.trac.backend import TracBackend


class TracBackendTestCase(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.trac = TracBackend()
	
	def test_get_ticket_list(self):
		request = self.factory.get('')
		tickets = self.trac.get_ticket_list(request)
		self.assertIsInstance(tickets, list)
	
	def test_get_ticket(self):
		pass


class FakeBasicAuthentication(BasicAuthentication):
	"""Pre-supplies the user/passwd dictionary that is used for checking passwords."""
	def __init__(self):
		self.hash = {
			# test:test
			'test': '7ryHh1B8eNNuM'
		}
		try:
			import crypt
			self.crypt = crypt.crypt
		except ImportError:
			try:
				import fcrypt
				self.crypt = fcrypt.crypt
			except ImportError:
				self.crypt = None
	
	def check_reload(self):
		pass



class TestTracAuthBackend(TracAuthBackend):
	def get_trac_auth(self):
		return FakeBasicAuthentication()


class TracAuthTestCase(TestCase):
	def setUp(self):
		self.auth = TestTracAuthBackend()
	
	def test_user_created(self):
		user = self.auth.authenticate('test', 'test')
		self.assertIsInstance(user, User)
		self.assertEqual(user.password, FAKE_PASSWORD)
	
	def test_no_user(self):
		user = self.auth.authenticate('test', 'wrong')
		self.assertEqual(user, None)
	
	def test_user_delete(self):
		"""Tests that a trac-created user will be deleted by the backend."""
		User.objects.create(username='to_del', password=FAKE_PASSWORD)
		user = self.auth.authenticate('to_del', 'who_cares')
		self.assertEqual(user, None)
		with self.assertRaises(User.DoesNotExist):
			User.objects.get(username='to_del')
	
	def test_user_no_delete(self):
		"""Tests that a django-created user will not be deleted by the backend."""
		User.objects.create(username='no_del', password='who_cares')
		user = self.auth.authenticate('no_del', 'other_passwd')
		self.assertEqual(user, None)
		try:
			User.objects.get(username='no_del')
		except User.DoesNotExist:
			raise AssertionError, "User no_del expected but not found."
