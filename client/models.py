from django.utils import timezone

from django.db import models
from account.models import CustomUser
from writer.models import Article




class Subscription(models.Model):
    PLAN_CHOICES=[
        ("FREE","Free"),
        ("PREMIUM","Premium"),
    ]

    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    plan=models.CharField(max_length=20,choices=PLAN_CHOICES, default="FREE")
    cost=models.DecimalField(max_digits=6, decimal_places=2,default=0)
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField(null=True, blank=True)



    def is_valid(self):
        return(
            self.plan=="PREMIUM" and 
            self.is_active and
            self.expires_at and
                self.expires_at > timezone.now()
        )
    



    def __str__(self):
        return f"{self.user.email} - {self.plan}"
    



class Payment(models.Model):
    STATUS_CHOICES=[
        ("PENDING","Pending"),
        ("COMPLETED","Completed"),
        ("FAILED","Failed"),
    ]

    

    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription=models.ForeignKey(Subscription, on_delete=models.CASCADE)
    paypal_order_id=models.CharField(max_length=255, blank=True, null=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    amount=models.DecimalField(max_digits=6, decimal_places=2)
    payment_date=models.DateTimeField(auto_now_add=True)
   


    def __str__(self):
        return f"{self.user.email} - {self.amount} on {self.payment_date}"
    





class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()

    parent=models.ForeignKey(
    'self', null=True,
      blank=True,
        on_delete=models.CASCADE, 
        related_name='replies')
    
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes=[
            models.Index(fields=['article', 'date_posted']),
        ]

    def __str__(self):
        return f"Comment by {self.user.email} - {self.article.title}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together=('user','article')
        indexes=[
            models.Index(fields=['article', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} likes {self.article.title}"
    









class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'article')
        indexes=[
            models.Index(fields=['article', 'created_at']),
        ]


    def __str__(self):
        return f"{self.user.email} bookmarked {self.article.title}"
    





class ArticleView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes=[
            models.Index(fields=['article', 'viewed_at']),
        ]

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
    link=models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message}"




