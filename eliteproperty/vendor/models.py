from django.db import models
from accounts.models import Account

class VendorProfile(models.Model):

    vendor = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile', blank=True, null=True)
    specialization = models.CharField(max_length=100, default='General')
    brokerage_fee = models.PositiveIntegerField(blank=True, null=True) 
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    year_of_experience = models.PositiveIntegerField(null=True, blank=True, default=0)
    age = models.PositiveIntegerField(blank=True, null=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.vendor)
