from django.db import models

from . managers import CustomUsermanager
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin

from django.utils import timezone



class CustomUser(AbstractBaseUser,PermissionsMixin):
    username=None
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=135)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(default=timezone.now)


    consent_given=models.BooleanField(default=False) # models for consent by default it is fasle unless user hit the content buton
    is_writer=models.BooleanField(default=False)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=CustomUsermanager()


    def __str__(self):
        return self.email






class EmailOtp(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)


    def is_valid(self):

        return timezone.now() < self.created_at + timezone.timedelta(minutes=10)
    







class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} Profile"
    




    

    