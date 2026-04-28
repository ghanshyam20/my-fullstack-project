from django.contrib.auth.forms import UserCreationForm

from django  import forms

from .models import CustomUser



class CreateUserForm(UserCreationForm):
    consent_given=forms.BooleanField(required=True,
                                     label="I agree to the Terms and Privacy Policy")
    
    class Meta:

        model=CustomUser
        fields=['email', 'first_name','last_name', 'password1','password2']


        



        