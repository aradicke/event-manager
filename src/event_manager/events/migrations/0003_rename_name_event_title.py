# Generated by Django 4.1 on 2023-07-19 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_location_event_category_delete_eventcategory_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='name',
            new_name='title',
        ),
    ]