import json

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Event, EventUpdate


@receiver(pre_save, sender=Event)
def update_tracker(sender, instance, **kwargs):
    print("Oh lawd he comin'")
    try:
        old_instance = Event.objects.values().get(id=instance.id)
        old_instance["created_at"] = old_instance["created_at"].strftime(
            "%Y/%m/%d %H:%M:%S.%f%z"
        )
        old_instance["start_time"] = old_instance["start_time"].strftime(
            "%Y/%m/%d %H:%M:%S.%f%z"
        )
        old_instance["end_time"] = old_instance["end_time"].strftime(
            "%Y/%m/%d %H:%M:%S.%f%z"
        )
        update = EventUpdate(event=instance, previous_values=json.dumps(old_instance))
        update.save()
    except Event.DoesNotExist:
        pass
