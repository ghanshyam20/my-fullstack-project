from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django  import forms

from .models import CustomUser



class CreateUserForm(UserCreationForm):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)

    consent_given=forms.BooleanField(required=True,
                                     label="I agree to the Terms and Privacy Policy")
    
    class Meta:

        model=CustomUser
        fields=['email', 'first_name','last_name', 'password1','password2']


        
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


        