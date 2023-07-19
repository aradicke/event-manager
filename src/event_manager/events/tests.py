import pytz
from datetime import datetime, timedelta

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from events.models import Event, Category, Location


class EventTests(TestCase):
    test_categories = [
        {"name": "Training", "description": "Learn things"},
        {"name": "Code Review", "description": "Bring ideas about loops"},
        {"name": "Social", "description": "There will be pizza"},
    ]
    test_locations = [
        {"name": "Bay Meeting Room", "description": "5 seats, one screen"},
        {"name": "Fjord Meeting Room", "description": "10 seats, no screen"},
        {"name": "Inlet Meeting Room", "description": "1 on 1 only"},
    ]

    test_records = [
        {
            "title": "Compliance Training",
            "description": "Don't violate HIPAA",
            "start_time": datetime.now(pytz.utc) + timedelta(hours=72),
            "end_time": datetime.now(pytz.utc) + timedelta(hours=73),
        },
        {
            "title": "Review Event Manager",
            "description": "Yes, there is a lot of boilerplate",
            "start_time": datetime.now(pytz.utc) + timedelta(days=72),
            "end_time": datetime.now(pytz.utc) + timedelta(hours=73),
            "category": "Code Review",
            "location": "Bay Meeting Room",
        },
        {
            "title": "Compliance Training",
            "description": "Don't violate HIPAA",
            "start_time": datetime.now(pytz.utc) + timedelta(hours=72),
            "end_time": datetime.now(pytz.utc) + timedelta(hours=73),
            "category": "Training",
            "location": "Bay Meeting Room",
        },
        {
            "title": "Sales Kickoff Pizza Party",
            "description": "Garlic knots will also be available",
            "start_time": datetime.now(pytz.utc) + timedelta(hours=72),
            "end_time": datetime.now(pytz.utc) + timedelta(hours=73),
            "category": "Social",
            "location": "Fjord Meeting Room",
        },
        {
            "title": "Performance Review",
            "description": "How do we feel about expectations?",
            "start_time": datetime.now(pytz.utc) + timedelta(hours=72),
            "end_time": datetime.now(pytz.utc) + timedelta(hours=73),
            "category": "Social",
            "location": "Inlet Meeting Room",
        },
    ]

    def setUp(self):
        self.client = APIClient()

    def test_categories_create(self):
        for category in self.test_categories:
            create = self.client.post(reverse("category-list"), category, format="json")
            self.assertEquals(create.status_code, 201)

        categories = Category.objects.all()
        self.assertEquals(len(categories), len(self.test_categories))

    def test_locations_create(self):
        for location in self.test_categories:
            create = self.client.post(reverse("location-list"), location, format="json")
            self.assertEquals(create.status_code, 201)

        locations = Location.objects.all()
        self.assertEquals(len(locations), len(self.test_locations))

    def test_events_create_and_destroy(self):
        create = self.client.post(
            reverse("event-list"), self.test_records[0], format="json"
        )
        self.assertEquals(create.status_code, 201)
        events = Event.objects.all()
        self.assertEquals(len(events), 1)

        destroy = self.client.delete(
            reverse("event-detail", kwargs={"pk": create.data["id"]}),
        )
        self.assertEquals(destroy.status_code, 204)
        events = Event.objects.all()
        self.assertEquals(len(events), 0)

    def test_list(self):
        self.load_categories_and_locations()
        for index, record in enumerate(self.test_records[1:]):
            record["category"] = Category.objects.filter(
                name=record["category"]
            ).first()
            record["location"] = Location.objects.filter(
                name=record["location"]
            ).first()
            event = Event(**record)
            event.start_time += timedelta(days=index)
            event.end_time += timedelta(days=index)
            event.save()

        self.assertEquals(Event.objects.count(), len(self.test_records[1:]))
        list_call = self.client.get(reverse("event-list"), format="json")
        self.assertEquals(list_call.status_code, 200)
        self.assertEquals(len(list_call.data), len(self.test_records[1:]))

    def test_retrieve_and_update(self):
        self.assertTrue(True)

    def load_categories_and_locations(self):
        for category in self.test_categories:
            category = Category(**category)
            category.save()

        for location in self.test_locations:
            location = Location(**location)
            location.save()

    # TODO Add failure cases
