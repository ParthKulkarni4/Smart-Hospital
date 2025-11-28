from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Bill, Payment
from .serializers import BillSerializer, PaymentSerializer

class BillViewSet(viewsets.ModelViewSet):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Order by latest bill
        return Bill.objects.all().order_by('-bill_date')

class PaymentViewSet(viewsets.ModelViewSet):
    """
    Endpoint specifically to Add Payments
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.all().order_by('-payment_date')

    def perform_create(self, serializer):
        # When a payment is added, the model's save() method 
        # will automatically update the Bill's balance.
        serializer.save()