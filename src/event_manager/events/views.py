from events.models import Event, Category, Location
from rest_framework import viewsets
from rest_framework import permissions
from events.serializers import EventSerializer, CategorySerializer, LocationSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    Basic event endpoint
    """

    queryset = Event.objects.all().order_by("-start_time")
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Manage categories for events
    """

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class LocationViewSet(viewsets.ModelViewSet):
    """
    Manage locations for events
    """

    queryset = Location.objects.all().order_by("name")
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
