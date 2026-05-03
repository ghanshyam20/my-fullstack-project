from django.contrib import admin
from .models import *


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__email', 'article__title')
    list_filter = ('created_at',)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__email', 'article__title')
    list_filter = ('created_at',)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'content', 'date_posted')
    search_fields = ('user__email', 'article__title', 'content')
    list_filter = ('date_posted',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'expires_at')
    search_fields = ('user__email',)
    list_filter = ('plan', 'is_active')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'payment_date')
    search_fields = ('user__email',)
    list_filter = ('status',)



@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'viewed_at')
    search_fields = ('user__email', 'article__title')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'reason', 'created_at')
    search_fields = ('user__email', 'article__title', 'reason')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')