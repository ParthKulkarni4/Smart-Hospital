# from rest_framework import viewsets, permissions
# from rest_framework.views import APIView
# from .models import Ambulance, AmbulanceTrip
# from .serializers import AmbulanceSerializer, AmbulanceTripSerializer
# from rest_framework.response import Response
# from rest_framework.decorators import action

# class AmbulanceAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self,request):
#         ambulances= Ambulance.objects.all()
#         serializer= AmbulanceSerializer(ambulances,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = AmbulanceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
    

# class AmbulanceTripViewSet(viewsets.ModelViewSet):
#     queryset = AmbulanceTrip.objects.select_related('ambulance','patient').all();
#     serializer_class = AmbulanceTripSerializer; 
#     permission_classes=[permissions.IsAuthenticated]

#     @action(detail=True, methods=['post'])
#     def set_dispatch(self, request, pk=None):
#         trip = self.get_object()
#         trip.status = 'dispatched'
#         serializer = self.get_serializer(trip, data={'status': 'dispatched'}, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Ambulance Dispatched", "data": serializer.data})
    

#     @action(detail=True, methods=["POST"])
#     def set_arrive(self, request, pk=None):
#         trip = self.get_object()
#         serializer = self.get_serializer(trip, data={"status": "arrived"}, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Ambulance Arrived at patient", "data": serializer.data})



#     @action(detail=True, methods=["POST"])
#     def set_complete(self, request, pk=None):
#         trip = self.get_object()
#         serializer = self.get_serializer(trip, data={"status": "completed"}, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Trip Completed", "data": serializer.data})






from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Ambulance, AmbulanceCall
from .serializers import AmbulanceSerializer, AmbulanceLocationSerializer, AmbulanceCallSerializer


# 🚑 Ambulance API
class AmbulanceViewSet(viewsets.ModelViewSet):
    queryset = Ambulance.objects.all()
    serializer_class = AmbulanceSerializer
    permission_classes = [IsAuthenticated]

    # DRIVER → Update location
    @action(detail=True, methods=['patch'])
    def update_location(self, request, pk=None):
        ambulance = self.get_object()
        serializer = AmbulanceLocationSerializer(ambulance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Location Updated",
                "lat": serializer.data.get('current_lat'),
                "long": serializer.data.get('current_long')
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🚑 Ambulance Calls API
class AmbulanceCallViewSet(viewsets.ModelViewSet):
    queryset = AmbulanceCall.objects.all().order_by('-created_at')
    serializer_class = AmbulanceCallSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user)

    # Assign ambulance
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        call = self.get_object()
        amb_id = request.data.get("ambulance_id")

        try:
            amb = Ambulance.objects.get(id=amb_id)
        except Ambulance.DoesNotExist:
            return Response({"error": "Ambulance not found"}, status=404)

        call.ambulance = amb
        call.status = "Dispatched"
        call.save()

        amb.status = "OnTrip"
        amb.save()

        return Response({"message": "Ambulance assigned successfully"})

    # Complete trip
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        call = self.get_object()
        call.status = "Completed"
        call.completed_at = timezone.now()
        call.save()

        if call.ambulance:
            call.ambulance.status = "Available"
            call.ambulance.save()

        return Response({"message": "Trip completed successfully"})

    # LIVE LOCATION API for patient & admin
    @action(detail=True, methods=['get'])
    def live_location(self, request, pk=None):
        call = self.get_object()

        if not call.ambulance:
            return Response({"error": "Ambulance not assigned"}, status=400)

        amb = call.ambulance

        return Response({
            "vehicle_number": amb.vehicle_number,
            "lat": amb.current_lat,
            "long": amb.current_long,
            "updated_at": amb.last_location_update
        })
