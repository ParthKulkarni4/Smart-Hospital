from rest_framework.routers import DefaultRouter
from .api_views import AmbulanceAPIView, AmbulanceTripViewSet
from django.urls import path, include
router = DefaultRouter();
router.register('trips', AmbulanceTripViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('vehicles/', AmbulanceAPIView.as_view(), name='ambulance_api'),
]
