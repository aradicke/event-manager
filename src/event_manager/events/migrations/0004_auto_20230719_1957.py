# Generated by Django 4.1 on 2023-07-19 19:57
from pathlib import Path
import json
from django.db import migrations
from django.conf import settings


def load_data(apps, schema_editor):
    Category = apps.get_model("events", "Category")
    Location = apps.get_model("events", "Location")
    # Event = apps.get_model("events", "Event")
    # strptime_string = "%Y-%m-%d %H:%M:%S.%f%z"
    # '2023-07-19 20:11:58.522887+0000'

    file_path = f"{Path(settings.BASE_DIR).parent.absolute()}/event_manager/qa_data/qa_data.json"
    with open(file_path, "r") as file:
        seeds = json.loads(file.read())

    for category in seeds["categories"]:
        work = Category(**category)
        work.save()

    for location in seeds["locations"]:
        work = Location(**location)
        work.save()


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0003_rename_name_event_title"),
    ]

    operations = [
        migrations.RunPython(code=load_data, reverse_code=migrations.RunPython.noop),
    ]


# python manage.py migrate events 0003_rename_name_event_title
