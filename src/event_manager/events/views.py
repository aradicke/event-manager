from events.models import Event
from rest_framework import viewsets
from rest_framework import permissions
from events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    Basic event endpoint
    """

    queryset = Event.objects.all().order_by("-start_time")
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
