from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Event(models.Model):
    name = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # TODO event_owner, event_category, event_location,

    def clean(self):
        super().clean()


class EventCategory(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()
