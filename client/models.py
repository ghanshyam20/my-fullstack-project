from django.db import models
from account.models import CustomUser
from writer.models import Article




class Subscription(models.Model):

    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    plan=models.CharField(max_length=100,choices=[('FREE','Free'),
                                                  ('PREMIUM','Premium')])
    cost=models.DecimalField(max_digits=6, decimal_places=2)
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return f"{self.user.email} - {self.plan}"
    



class Payment(models.Model):

    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription=models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=6, decimal_places=2)
    payment_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=[
        ('PENDING','Pending'),
        ('COMPLETED','Completed'),
        ('FAILED','Failed') 
    ],default='PENDING')


    def __str__(self):
        return f"{self.user.email} - {self.amount} on {self.payment_date}"
    





class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} - {self.article.title}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together=('user','article')

    def __str__(self):
        return f"{self.user.email} likes {self.article.title}"
    









class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'article')


    def __str__(self):
        return f"{self.user.email} bookmarked {self.article.title}"
    





class ArticleView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} viewed {self.article.title}"



class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')


    def __str__(self):
        return f"{self.user.email} reported {self.article.title}"
    
    

  




class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)




