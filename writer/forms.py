from django import forms
from django.forms import ModelForm

from .models import Article
from account.models import CustomUser


# article  form for writer
class ArticleForm(ModelForm):

    ARTICLE_TYPE_CHOICES = (
        ('False', 'Free Article'),
        ('True', 'Premium Article'),
    )

    is_premium = forms.ChoiceField(
        choices=ARTICLE_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Article Type"
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Write your article here...'
            }),
        }

    def clean_is_premium(self):
        value = self.cleaned_data.get('is_premium')
        return value == 'True'


# user update 
class UpdateUserForm(ModelForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        exclude = ['password1', 'password2']


# article update form 
class UpdateArticleForm(forms.ModelForm):

    ARTICLE_TYPE_CHOICES = (
        ('False', 'Free Article'),
        ('True', 'Premium Article'),
    )

    is_premium = forms.ChoiceField(
        choices=ARTICLE_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Article Type"
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8
            }),
        }

    def clean_is_premium(self):
        value = self.cleaned_data.get('is_premium')
        return value == 'True'