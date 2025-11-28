from rest_framework.routers import DefaultRouter
from .api_views import ReceptionistProfileViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('receptionists', ReceptionistProfileViewSet, basename='api-receptionist')

urlpatterns = [
    path('', include(router.urls)),
]
