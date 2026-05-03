from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, UpdateUserForm
from .models import Article, ArticleImage
from django.contrib import messages
from django.db import transaction

def is_writer_only(request):
    return request.user.is_writer and not request.user.is_staff

def is_client_only(request):
    return not request.user.is_writer and not request.user.is_staff







@login_required(login_url='my-login')
def writer_dasboard(request):
    # block access for normal user 
    if is_client_only(request):
        return redirect('client-dashboard')

    total_articles = Article.objects.filter(user=request.user).count()
    premium_articles = Article.objects.filter(user=request.user, is_premium=True).count()
    free_articles = Article.objects.filter(user=request.user, is_premium=False).count()
    recent_articles = Article.objects.filter(user=request.user).order_by('-date_posted')[:5]

    context = {
        'total_articles': total_articles,
        'premium_articles': premium_articles,
        'free_articles': free_articles,
        'recent_articles': recent_articles,
    }

    return render(request, 'writer/writer-dashboard.html', context)





@login_required(login_url='my-login')
def create_article(request):
    if is_client_only(request):
        return redirect('client-dashboard')

    form = ArticleForm()

    if request.method == 'POST':
        
        print("FILES:", request.FILES)

        data = request.POST.copy()
        data['content'] = request.POST.get('content', '').strip()

        form = ArticleForm(data, request.FILES)

        if form.is_valid():

            try:
                with transaction.atomic():

                    article = form.save(commit=False)
                    article.user = request.user
                    article.save()

                    files = request.FILES.getlist('images')

                    for file in files:
                        #  basic validation
                        if file.content_type.startswith('image/'):
                            img=ArticleImage.objects.create(
                                article=article,
                                image=file
                            )

                            print("IMAGE CREATED:", img)
                            print("URL:", img.image.url)


                messages.success(request, "Article published successfully!")
                return redirect('my-articles')

            except Exception as e:
                messages.error(request, "Something went wrong. Try again.")

        else:
            messages.error(request, "Please fix the form errors.")

    context = {'CreateArticleForm': form}
    return render(request, 'writer/create-article.html', context)



@login_required(login_url='my-login')
def my_articles(request):
    if is_client_only(request):
        return redirect('client-dashboard')
   

    articles = Article.objects.filter(user=request.user)

    context = {'AllArticles': articles}
    return render(request, 'writer/my-articles.html', context)



@login_required(login_url='my-login')
def update_article(request, pk):
    if is_client_only(request):
        return redirect('client-dashboard')

    try:
        article = Article.objects.get(id=pk, user=request.user)
    except Article.DoesNotExist:
        messages.error(request, "Article not found.")
        return redirect('my-articles')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            article = form.save()

            # handle new uploaded images
            files = request.FILES.getlist('images')

            for file in files:
                # basic validation (safe)
                if file.content_type.startswith('image/'):
                    ArticleImage.objects.create(
                        article=article,
                        image=file
                    )

            messages.success(request, "Article updated successfully!")  
            return redirect('my-articles')

        else:
            messages.error(request, "Please fix the form errors.")

    else:
        form = ArticleForm(instance=article)

    context = {
        'UpdateArticleForm': form,
        'article': article
    }

    return render(request, 'writer/update-article.html', context)

    



@login_required(login_url='my-login')
def delete_article(request, pk):

    if is_client_only(request):
        return redirect('client-dashboard')

    try:
        article = Article.objects.get(id=pk, user=request.user)
    except Article.DoesNotExist:
        return redirect('my-articles')

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article deleted successfully!")
        return redirect('my-articles')

    return render(request, 'writer/delete-article.html')



@login_required(login_url='my-login')
def delete_image(request, pk):
    if is_client_only(request):
        return redirect('client-dashboard')

    try:
        image = ArticleImage.objects.get(id=pk, article__user=request.user)
        article_id = image.article.id
        image.delete()
        messages.success(request, "Image deleted successfully!")

        return redirect('update-article', pk=article_id)

    except ArticleImage.DoesNotExist:
        return redirect('my-articles')



# @login_required(login_url='my-login')
# def account_management(request):

#     form = UpdateUserForm(instance=request.user)

#     if request.method == 'POST':
#         form = UpdateUserForm(request.POST, instance=request.user)

#         if form.is_valid():
#             form.save()
#             return redirect('writer-dashboard')

#     context = {'UpdateUserForm': form}
#     return redirect('profile-page')



# from django.core.files.storage import default_storage

# print("STORAGE:", default_storage.__class__)