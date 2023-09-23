from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, phone_number, password=None):
        if not email:
            raise TypeError("User must have an Email Address!")
        if not username:
            raise TypeError("User must have an Username!")
        if not phone_number:
            raise TypeError("User must have a Phone Number!")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            phone_number = phone_number
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, first_name, last_name, email, username, phone_number, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            phone_number = phone_number,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user_type = UserType.objects.get(user_type_name = 'Admin')
        user.user_type = user_type
        user.save(using=self._db)
        return user
    

class UserType(models.Model):
    user_type_name = models.CharField(max_length=10)

    def __str__(self):
        return self.user_type_name
    

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True, related_name='user_type')
    email = models.EmailField(unique=True, db_index=True, null=False)
    phone_number = models.CharField(unique=True, blank=True, max_length=10)
    username = models.CharField(unique=True, blank=True, max_length=50)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_profile   = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
