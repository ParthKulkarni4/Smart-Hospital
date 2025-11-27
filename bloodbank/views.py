# bloodbank/views.py

from rest_framework import viewsets, status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import BloodDonor, BloodBag, BloodRequest

from .serializers import BloodDonorSerializer, BloodBagSerializer, BloodRequestSerializer
 
class BloodDonorViewSet(viewsets.ModelViewSet):

    serializer_class = BloodDonorSerializer

    permission_classes = [IsAuthenticated]

    queryset = BloodDonor.objects.all()
 
class BloodBagViewSet(viewsets.ModelViewSet):

    serializer_class = BloodBagSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Allow filtering by status (e.g., ?status=Available)

        queryset = BloodBag.objects.all()

        status_param = self.request.query_params.get('status')

        group_param = self.request.query_params.get('group')

        if status_param:

            queryset = queryset.filter(status=status_param)

        if group_param:

            queryset = queryset.filter(blood_group=group_param)

        return queryset
 
class BloodRequestViewSet(viewsets.ModelViewSet):

    serializer_class = BloodRequestSerializer

    permission_classes = [IsAuthenticated]

    queryset = BloodRequest.objects.all().order_by('-request_date')
 
    def perform_update(self, serializer):

        # Custom logic for issuing blood

        instance = serializer.instance

        new_status = serializer.validated_data.get('status')

        issued_bag = serializer.validated_data.get('issued_bag')
 
        if new_status == 'Issued' and issued_bag:

            # 1. Check if bag is actually available

            if issued_bag.status != 'Available':

                raise serializer.ValidationError("Selected blood bag is not available.")

            # 2. Update Bag Status

            issued_bag.status = 'Issued'

            issued_bag.save()

            # 3. Save Request

            serializer.save()

        else:

            serializer.save()
 
