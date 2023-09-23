from django.db import models
from accounts.models import Account
from property.models import Property


class UserProfile(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_pictures', blank=True)
    about = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True) 
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(blank=True, null=True,default=False)
    vendor = models.ForeignKey(Account, related_name='vendor', on_delete=models.CASCADE, null=True, blank=True)
   

    def __str__(self):
        return str(self.user)
