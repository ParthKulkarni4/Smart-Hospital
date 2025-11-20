from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RadiologyTestViewSet,
    RadiologyReportViewSet,
    RadiologyRecordViewSet,
    radiology_home,
)

router = DefaultRouter()
router.register(r"tests", RadiologyTestViewSet, basename="radiologytest")
router.register(r"reports", RadiologyReportViewSet, basename="radiologyreport")
router.register(r"records", RadiologyRecordViewSet, basename="radiologyrecord")

urlpatterns = [
    path("", radiology_home, name="radiology_home"),     # Dashboard Home
    path("api/", include(router.urls)),                 # API URLs
]
