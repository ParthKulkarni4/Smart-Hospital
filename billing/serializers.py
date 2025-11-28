from rest_framework import serializers
from .models import Bill, BillItem, Payment
from patient.serializers import PatientSerializer

class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = ['id', 'item_name', 'quantity', 'unit_price', 'amount']
        read_only_fields = ['amount'] # Calculated automatically

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'payment_mode', 'bill','remarks']

class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True,required=False)    # Nested items    
    payments = PaymentSerializer(many=True, read_only=True) # View payments
    patient_details = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id', 'patient', 'patient_details', 'doctor', 
            'bill_date', 'total_amount', 'paid_amount', 
            'balance_amount', 'status', 'items', 'payments'
        ]
        read_only_fields = ['total_amount', 'paid_amount', 'balance_amount', 'status']

    def create(self, validated_data):
        """
        Custom Create to handle Nested BillItems
        """
        # items_data = validated_data.pop('items')
        items_data = validated_data.pop('items', [])
        bill = Bill.objects.create(**validated_data)
        
        for item_data in items_data:
            BillItem.objects.create(bill=bill, **item_data)
        
        # Trigger calculation
        bill.update_balances()
        return bill