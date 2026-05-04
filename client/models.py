from django.utils import timezone
from django.db import models
from account.models import CustomUser
from writer.models import Article


# subcription 

class Subscription(models.Model):
    PLAN_CHOICES = [
        ("FREE", "Free"),
        ("PREMIUM", "Premium"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="FREE")
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return (
            self.plan == "PREMIUM"
            and self.is_active
            and self.expires_at is not None
            and self.expires_at > timezone.now()
        )

    def remaining_days(self):
        if self.expires_at:
            return max((self.expires_at - timezone.now()).days,0)
        return 0

    def __str__(self):
        return f"{self.user.email} - {self.plan}"

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["created_at"]),
        ]


#payemnt 

class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)

    paypal_order_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payer_email = models.EmailField(null=True, blank=True)

    def is_successful(self):
        return self.status == "COMPLETED"

    def __str__(self):
        return f"{self.user.email} - {self.amount} on {self.payment_date}"

    class Meta:
        indexes = [
            models.Index(fields=["paypal_order_id"]),
            models.Index(fields=["user", "payment_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payer_email"]),
            
        ]
        ordering = ["-payment_date"]


# comment 

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='article_comments')

    content = models.TextField()

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.article.title}"

    class Meta:
        indexes = [
            models.Index(fields=['article', 'date_posted']),
        ]
        ordering = ['-date_posted']


# like 

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='article_likes')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} likes {self.article.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_like')
        ]
        indexes = [
            models.Index(fields=['article', 'created_at']),
        ]


# Bookmark 

class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='article_bookmarks')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} bookmarked {self.article.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_bookmark')
        ]
        indexes = [
            models.Index(fields=['article', 'created_at']),
        ]


# article view

class ArticleView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_views')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='article_views')

    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} viewed {self.article.title}"

    class Meta:
        indexes = [
            models.Index(fields=['article', 'viewed_at']),
        ]
        ordering = ['-viewed_at']


# report 

class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_reports')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='article_reports')

    reason = models.TextField()  # upgraded
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} reported {self.article.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_report')
        ]
        indexes = [
            models.Index(fields=['article', 'created_at']),
        ]


# notification 

class Notification(models.Model):
    TYPE_CHOICES = [
        ("COMMENT", "Comment"),
        ("LIKE", "Like"),
        ("PAYMENT", "Payment"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')

    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="COMMENT")

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.message}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]