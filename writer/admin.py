from django.contrib import admin
from .models import Article, ArticleImage, Category, Tag, ArticleTag


class ArticleImageInline(admin.TabularInline):  # or StackedInline
    model = ArticleImage
    extra = 3   # number of empty upload fields


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ArticleTag)
admin.site.register(ArticleImage)
