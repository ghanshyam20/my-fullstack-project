from .models import Article


from django.forms import ModelForm




class ArticleForm(ModelForm):
    class Meta:


        model=Article
        fields=['title', 'content', 'is_premium']


