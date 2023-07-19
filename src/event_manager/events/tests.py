from django.test import TestCase
from rest_framework.test import APIClient
from events.models import Event
from datetime import datetime, timedelta, timezone


class EventTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def SmokeTest(self):
        self.assertTrue(True)

    def test_create(self):
        parms = {
            "name": "Compliance Training",
            "description": "Don't violate HIPAA",
            "start_time": null,
            "end_time": null,
        }

    def test_destroy(self):
        self.assertTrue(False)

    def test_list(self):
        self.assertTrue(False)

    def test_retrieve(self):
        self.assertTrue(False)

    def test_update(self):
        # test partial and full update
        self.assertTrue(False)
