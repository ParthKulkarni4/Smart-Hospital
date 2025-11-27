from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet

router = DefaultRouter()
router.register('user', RegisterUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
