# from rest_framework.routers import DefaultRouter
# from .api_views import AmbulanceAPIView, AmbulanceTripViewSet
# from django.urls import path, include
# router = DefaultRouter();
# router.register('trips', AmbulanceTripViewSet)


# urlpatterns = [
#     path('', include(router.urls)),
#     path('vehicles/', AmbulanceAPIView.as_view(), name='ambulance_api'),
# ]




# ambulance/urls.py

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .api_views import AmbulanceViewSet, AmbulanceCallViewSet
 
router = DefaultRouter()

router.register(r'vehicles', AmbulanceViewSet, basename='ambulance')

router.register(r'calls', AmbulanceCallViewSet, basename='ambulance-call')
 
urlpatterns = [

    path('', include(router.urls)),

]
 