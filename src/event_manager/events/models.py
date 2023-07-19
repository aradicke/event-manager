from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Event(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.ForeignKey(
        "events.Category", null=True, on_delete=models.SET_NULL
    )
    location = models.ForeignKey(
        "events.Location", null=True, on_delete=models.SET_NULL
    )

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError("Start time must come before end time")
        super().clean()


class Category(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} id:{self.id}"


class Location(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} id:{self.id}"
