from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from .models import Ambulance, AmbulanceTrip
from .serializers import AmbulanceSerializer, AmbulanceTripSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class AmbulanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        ambulances= Ambulance.objects.all()
        serializer= AmbulanceSerializer(ambulances,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = AmbulanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class AmbulanceTripViewSet(viewsets.ModelViewSet):
    queryset = AmbulanceTrip.objects.select_related('ambulance','patient').all();
    serializer_class = AmbulanceTripSerializer; 
    permission_classes=[permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def set_dispatch(self, request, pk=None):
        trip = self.get_object()
        trip.status = 'dispatched'
        serializer = self.get_serializer(trip, data={'status': 'dispatched'}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Ambulance Dispatched", "data": serializer.data})
    

    @action(detail=True, methods=["POST"])
    def set_arrive(self, request, pk=None):
        trip = self.get_object()
        serializer = self.get_serializer(trip, data={"status": "arrived"}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Ambulance Arrived at patient", "data": serializer.data})



    @action(detail=True, methods=["POST"])
    def set_complete(self, request, pk=None):
        trip = self.get_object()
        serializer = self.get_serializer(trip, data={"status": "completed"}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Trip Completed", "data": serializer.data})


