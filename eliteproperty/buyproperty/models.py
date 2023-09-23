from django.db import models
from accounts.models import Account
from property.models import Property


# Create your models here.

#Model for buying Renting Property

class RentBooking(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    payment_status = models.BooleanField(default=False)
    cancellation_policy = models.TextField()


#Model for buying Sale Property

class Interest(models.Model):

    PROPERTY_STATUS_CHOICES = (
    ('sold', 'Sold'),
    ('available', 'Available'),
)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=False)
    initial_deposit = models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2)
    property_status = models.CharField(max_length=20, choices=PROPERTY_STATUS_CHOICES, null=True, blank=True)
    is_paid=models.BooleanField(default=False)
        
       
          
#Model for payment 

class Order(models.Model):
    order_property = models.CharField(max_length=100)
    deposit_amount = models.CharField(max_length=25)
    order_id = models.CharField(max_length=100, default="")
    is_paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.order_property

class PropertyBooking(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, limit_choices_to={"is_active": True})
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="complete")
    booking_payment_id = models.CharField(max_length=100)
    booking_order_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now=True)
    deposit_amount = models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2) 
        
    def __str__(self):
        return f"Booking #{self.pk} - User: {self.user.username}, Property: {self.property.title}"


class RentPropertyBooking(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, limit_choices_to={"is_active": True})
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="complete")
    booking_payment_id = models.CharField(max_length=100)
    booking_order_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10,blank=True,null=True, decimal_places=2) 
        
    def __str__(self):
        return f"Booking #{self.pk} - User: {self.user.username}, Property: {self.property.title}"