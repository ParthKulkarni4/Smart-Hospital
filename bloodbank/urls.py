# bloodbank/urls.py

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import BloodDonorViewSet, BloodBagViewSet, BloodRequestViewSet
 
router = DefaultRouter()

router.register(r'donors', BloodDonorViewSet, basename='blood-donor')

router.register(r'bags', BloodBagViewSet, basename='blood-bag')

router.register(r'requests', BloodRequestViewSet, basename='blood-request')
 
urlpatterns = [

    path('', include(router.urls)),

]
 
