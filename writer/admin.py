from django.contrib import admin
from .models import Article, ArticleImage, Category, Tag, ArticleTag


#artcile image 
class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'is_premium', 'date_posted')
    search_fields = ('title', 'user__email')
    list_filter = ('is_premium', 'category', 'date_posted')
    inlines = [ArticleImageInline]



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag')
    search_fields = ('article__title', 'tag__name')



@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article',)