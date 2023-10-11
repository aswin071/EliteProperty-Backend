from django.db import models
from accounts.models import Account
from property.models import Property
from datetime import date



class AdminPayment(models.Model):
    vendor = models.ForeignKey(Account, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today) 

    def __str__(self):
        return f"Payment of ${self.amount} for Property {self.property} by Vendor {self.vendor} on {self.date}"
    