from events.models import Event, Category, Location, EventUpdate
from rest_framework import serializers


class EventUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventUpdate
        fields = ["id", "event", "created_at", "user", "previous_values"]


class EventUpdateMiniSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="eventupdate-detail", read_only=True
    )

    class Meta:
        model = EventUpdate
        fields = ["created_at", "previous_values", "detail_url"]


class EventSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="event-detail", read_only=True
    )
    updates = EventUpdateMiniSerializer(
        many=True, source="eventupdate_set", read_only=True
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "detail_url",
            "title",
            "description",
            "start_time",
            "end_time",
            "location",
            "category",
            "updates",
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
        fields = ["id", "name", "description"]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "description"]
