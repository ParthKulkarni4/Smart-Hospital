from django.urls import path
from . import views
urlpatterns = [path('', views.index, name='bloodbank_index')]

# bloodbank/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonorViewSet, BloodInventoryViewSet, IssueBloodAPIView, UsageReportAPIView, SummaryReportAPIView

router = DefaultRouter()
router.register(r'donors', DonorViewSet, basename='donor')
router.register(r'inventory', BloodInventoryViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
    path('issue/', IssueBloodAPIView.as_view(), name='blood-issue'),
    path('usage/', UsageReportAPIView.as_view(), name='blood-usage'),
    path('reports/summary/', SummaryReportAPIView.as_view(), name='blood-summary'),
]