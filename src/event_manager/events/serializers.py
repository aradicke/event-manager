from events.models import Event, Category, Location
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "location",
            "category",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.location:
            data["location_name"] = instance.location.name
        else:
            data["location_name"] = "no location given"
        if instance.category:
            data["category_name"] = instance.category.name
        else:
            data["category_name"] = "no category given"
        return data


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "description"]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ["name", "description"]
