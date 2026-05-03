from django.db import models
from django.core.mail import send_mail
from django.conf import settings



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

    writer_reason = models.TextField(blank=True)
    consent_given=models.BooleanField(default=False) # models for consent by default it is fasle unless user hit the content buton
    consent_timestamp=models.DateTimeField(null=True, blank=True)
    is_writer=models.BooleanField(default=False)
    is_writer_requested=models.BooleanField(default=False)



    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=CustomUsermanager()


    def __str__(self):
        return self.email
    

    def save(self, *args, **kwargs):

        if self.pk:
            old_user = CustomUser.objects.filter(pk=self.pk).first()
        else:
            old_user = None

        super().save(*args, **kwargs)

        #  this will trigegr send email when admin approves writer 
        if old_user and not old_user.is_writer and self.is_writer:
            
                login_link=f"{settings.SITE_URL}/my-login/"

                send_mail(
                    subject="Your Writer Application is Approved - InsightHub",
                    message=(
                        f"Hi {self.first_name},\n\n"
                        "Great news! Your writer application has been approved.\n\n"
                        "Welcome on the board !! Have a great journey.\n\n"
                        f"login here : {login_link}\n\n"
                        "Best of luck on your journey .\n\n"
                        "Ghanshyam Bhattarai "
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[self.email],
                    fail_silently=True,
                )

        






class EmailOtp(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)


    def is_valid(self):

        return timezone.now() < self.created_at + timezone.timedelta(minutes=10)
    







class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    #profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} Profile"
    



    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"




    























    

    