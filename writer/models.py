from django.db import models
from account.models import CustomUser
# for the Article 



class Article(models.Model):

    title=models.CharField(max_length=200)
    content=models.TextField(max_length=10000)
   
    date_posted=models.DateTimeField(auto_now_add=True)
    is_premium=models.BooleanField(default=False,verbose_name="Is this a  Premium Article?")
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    category=models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
    

class ArticleImage(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='articles/')

    def __str__(self):
        return f"Image for {self.article.title}"
    


class Category(models.Model):
    name=models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    


class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class ArticleTag(models.Model):
    article=models.ForeignKey(Article, on_delete=models.CASCADE)
    tag=models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.article.title} - {self.tag.name}"    
    




    






