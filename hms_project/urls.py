from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Your modules
    path('api/patient', include('patient.urls')),
    path('api/doctor', include('doctor.urls')),
    path('api/appointments', include('appointments.urls')),
    path('api/billing', include('billing.urls')),
    path('api/bloodbank', include('bloodbank.urls')),   # ← from PRIYANKAK

    # V1.00.00 modules
    path('api/ambulance', include('ambulance.api_urls')),
    path('api/frontoffice/', include('frontoffice.api_urls')),
]

   