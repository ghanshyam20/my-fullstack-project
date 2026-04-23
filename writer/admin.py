from django.contrib import admin
from .models import Article, ArticleImage


class ArticleImageInline(admin.TabularInline):  # or StackedInline
    model = ArticleImage
    extra = 3   # number of empty upload fields


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline]


admin.site.register(Article, ArticleAdmin)