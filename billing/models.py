from django.db import models
from patient.models import Patient
from doctor.models import Doctor

class Bill(models.Model):
    PAYMENT_STATUS = [
        ('Unpaid', 'Unpaid'),
        ('Partial', 'Partially Paid'),
        ('Paid', 'Paid'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    # Optional: Link to a doctor if this bill is for a specific consultation
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    
    bill_date = models.DateTimeField(auto_now_add=True)
    
    # Financials
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Unpaid')

    def __str__(self):
        return f"Bill #{self.id} - {self.patient.first_name}"

    def update_balances(self):
        """
        Helper to recalculate status based on items and payments.
        """
        # 1. Calculate Total from Items
        items_total = sum(item.amount for item in self.items.all())
        self.total_amount = items_total

        # 2. Calculate Total Paid from Payments
        payments_total = sum(pay.amount for pay in self.payments.all())
        self.paid_amount = payments_total

        # 3. Update Balance
        self.balance_amount = self.total_amount - self.paid_amount

        # 4. Update Status
        if self.balance_amount <= 0:
            self.status = 'Paid'
            self.balance_amount = 0 # Prevent negative balance
        elif self.paid_amount > 0:
            self.status = 'Partial'
        else:
            self.status = 'Unpaid'
        
        self.save()


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200) # e.g., "Consultation Fee"
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2) # qty * price

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Update parent bill total
        self.bill.update_balances()


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=50, default="Cash") # Cash, Card, UPI
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update parent bill balance
        self.bill.update_balances()