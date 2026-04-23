from django import forms

from django.forms import ModelForm

from .models import Article
from account.models import CustomUser




class ArticleForm(ModelForm):
    class Meta:


        model=Article
        fields=['title', 'content',  'is_premium']

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
            'is_premium':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


class UpdateUserForm(ModelForm):
    password=None
    class Meta:
        model=CustomUser
        fields=['email','first_name','last_name',]
        exclude=['password1','password2',]


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium' ]

