from django.contrib import admin


from .models import (
    Subscription, Payment, Comment,
    Like, Bookmark, ArticleView,
    Report, Notification
)

admin.site.register(Subscription)
admin.site.register(Payment)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Bookmark)
admin.site.register(ArticleView)
admin.site.register(Report)
admin.site.register(Notification)