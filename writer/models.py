from django.db import models
from account.models import CustomUser



# for the Article 



class Article(models.Model):

    title=models.CharField(max_length=200)
    content=models.TextField(max_length=10000)
    date_posted=models.DateTimeField(auto_now_add=True)
    is_premium=models.BooleanField(default=False,verbose_name="Is this a  Premium Article?")
    user=models.ForeignKey(CustomUser,max_length=10,on_delete=models.CASCADE, null=True)


