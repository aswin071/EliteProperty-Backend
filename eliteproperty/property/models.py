from django.db import models
from vendor.models import VendorProfile
from django.utils.timezone import now
from accounts.models import Account

class Property(models.Model):
    PROPERTY_TYPES = (
        ('Rent', 'For Rent'),
        ('Sale', 'For Sale'),
    )

    PROPERTY_STATUS = (
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Sold', 'Sold'),
    )


    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(choices=PROPERTY_TYPES, max_length=4)
    location = models.CharField(max_length=255)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()
    property_size = models.PositiveIntegerField()
    vendor = models.ForeignKey(Account, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    image2 = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    image3 = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    is_published=models.BooleanField(default=True)
    list_date=models.DateTimeField(default=now,blank=True)
    status = models.CharField(choices=PROPERTY_STATUS, default='Available', max_length=20)

    
    def __str__(self):      
        return self.title
