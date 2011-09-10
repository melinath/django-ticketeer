from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import unittest

from ticketeer.backends.trac013 import TracBackend


class TracBackendTestCase(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.trac = TracBackend()
	
	def test_get_ticket_list(self):
		request = self.factory.get('')
		tickets = self.trac.get_ticket_list(request)
		self.assertIsInstance(tickets, list)
