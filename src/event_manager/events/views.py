from django.contrib.postgres.search import SearchVector
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from events.serializers import EventSerializer, CategorySerializer, LocationSerializer
from events.models import Event, Category, Location


class EventViewSet(viewsets.ModelViewSet):
    """
    Basic event endpoint
    """

    queryset = Event.objects.all().order_by("-start_time")
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"])
    def search(self, request, *args, **kwargs):
        search_term = request.query_params.get("search_term")
        if not search_term:
            return Response(
                {"error": "A search term is required as a query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        evento = (
            self.get_queryset()
            .annotate(search=SearchVector("title", "description"))
            .filter(search=search_term)
        )
        serializer = self.get_serializer(evento, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
