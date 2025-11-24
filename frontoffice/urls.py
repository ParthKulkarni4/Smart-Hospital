from django.urls import path
from . import views
from patient import views as patient_views
from ambulance import views as ambulance_views

app_name = 'frontoffice'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.role_dashboard, name='role_dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    # path('patients/<int:pk>/', patient_views.patient_detail, name='patient_detail'),
    path('ambulance/', ambulance_views.index, name='ambulance_index'),
    path('ambulance/trips/', ambulance_views.trips, name='ambulance_trips'),
    path('ambulance/create-trip/', ambulance_views.create_trip, name='create_trip'),
]
