from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='ambulance_index'),
    path('trips/', views.trips, name='ambulance_trips'),
    path('create-trip/', views.create_trip, name='create_trip'),
]
