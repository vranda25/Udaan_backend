from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contact_no = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    is_business = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.is_business:
            return str(self.id)+') '+'business : '+self.email
        elif self.is_customer:
            return str(self.id)+') '+'customer : ' + self.email
        else:
            return str(self.id)+') '+self.email
