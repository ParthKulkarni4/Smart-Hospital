from django.shortcuts import render

def index(request):
    return render(request, 'bloodbank/index.html')

# bloodbank/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Sum
from .models import Donor, BloodInventory, BloodIssue
from .serializers import DonorSerializer, BloodInventorySerializer, BloodIssueSerializer
from .permissions import IsBloodBankStaff
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
# from rest_framework.permissions import AllowAny


class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all().order_by('-created_at')
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated, IsBloodBankStaff]
    # permission_classes = [AllowAny]


class BloodInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for inventory listing.
    Use a custom action for update/adjust.
    """
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    permission_classes = [IsAuthenticated, IsBloodBankStaff]
    # permission_classes = [AllowAny]

    @action(detail=True, methods=['put'], url_path='adjust', url_name='adjust')
    def adjust(self, request, pk=None):
        """
        Adjust inventory for a specific blood_group instance.
        Payload: { "units": 5.0 }  (this replaces the units value or you could add 'operation': 'add' )
        """
        inv = self.get_object()
        units = request.data.get('units')
        try:
            units = Decimal(str(units))
        except Exception:
            return Response({"detail": "Invalid units."}, status=status.HTTP_400_BAD_REQUEST)

        if units < 0:
            return Response({"detail": "Units cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)

        inv.units = units
        inv.save()
        return Response(self.get_serializer(inv).data, status=status.HTTP_200_OK)


class IssueBloodAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBloodBankStaff]
    # permission_classes = [AllowAny]

    def get(self, request):
        """Return list of all issued blood records."""
        issues = BloodIssue.objects.all().order_by('-id')
        serializer = BloodIssueSerializer(issues, many=True)
        return Response(serializer.data, status=200)
    @transaction.atomic
    def post(self, request):
        """
        Issue blood to patient:
        required: patient, blood_group, units_issued
        optional: issued_by (defaults to request.user), bill_no, remarks
        """
        serializer = BloodIssueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blood_group = serializer.validated_data['blood_group']
        units_to_issue = serializer.validated_data['units_issued']

        inventory = BloodInventory.objects.select_for_update().filter(blood_group=blood_group).first()
        if not inventory:
            return Response({"detail": f"No inventory item found for group {blood_group}"}, status=400)

        if inventory.units < units_to_issue:
            return Response({"detail": "Insufficient units in inventory."}, status=400)

        # subtract and create issue in atomic transaction
        inventory.units = inventory.units - units_to_issue
        inventory.save()

        issue = serializer.save(issued_by=request.user if not serializer.validated_data.get('issued_by') else serializer.validated_data.get('issued_by'))
        out_serializer = BloodIssueSerializer(issue)
        return Response(out_serializer.data, status=201)


class UsageReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBloodBankStaff]
    # permission_classes = [AllowAny]

    def get(self, request):
        """
        Returns total used per blood group and totals.
        """
        usage = BloodIssue.objects.values('blood_group').annotate(total_used=Sum('units_issued')).order_by('blood_group')
        total_issued = BloodIssue.objects.aggregate(total=Sum('units_issued'))['total'] or 0
        return Response({
            "usage_by_group": usage,
            "total_issued": total_issued
        })


class SummaryReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBloodBankStaff]
    # permission_classes = [AllowAny]

    def get(self, request):
        total_donors = Donor.objects.count()
        inventory = BloodInventory.objects.all()
        inventory_data = {inv.blood_group: float(inv.units) for inv in inventory}
        total_units_in_stock = sum(inv.units for inv in inventory)
        total_issued = BloodIssue.objects.aggregate(total=Sum('units_issued'))['total'] or 0
        return Response({
            "total_donors": total_donors,
            "inventory": inventory_data,
            "total_units_in_stock": float(total_units_in_stock),
            "total_issued": float(total_issued)
        })
