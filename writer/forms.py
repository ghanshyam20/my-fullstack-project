from .models import Article, ArticleImage
from account.models import CustomUser

from django.forms import ModelForm



class ArticleForm(ModelForm):
    class Meta:


        model=Article
        fields=['title', 'content', 'image', 'is_premium']


class UpdateUserForm(ModelForm):
    password=None
    class Meta:
        model=CustomUser
        fields=['email','first_name','last_name',]
        exclude=['password1','password2',]

