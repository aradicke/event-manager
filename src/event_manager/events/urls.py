from django.urls import include, path
from rest_framework import routers
from events import views

router = routers.DefaultRouter()
router.register(r"events", views.EventViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"locations", views.LocationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
