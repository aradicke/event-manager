from django.urls import include, path
from rest_framework import routers
from events import views

router = routers.DefaultRouter()
router.register(r"events", views.EventViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
