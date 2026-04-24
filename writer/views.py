from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ArticleForm, UpdateUserForm
from .models import Article, ArticleImage




@login_required(login_url='my-login')
def writer_dasboard(request):
    return render(request, 'writer/writer-dashboard.html')



@login_required(login_url='my-login')
def create_article(request):

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()

            # handle multiple images
            files = request.FILES.getlist('images')
            for file in files:
                ArticleImage.objects.create(article=article, image=file)

            return redirect('my-articles')

    context = {'CreateArticleForm': form}
    return render(request, 'writer/create-article.html', context)



@login_required(login_url='my-login')
def my_articles(request):

    articles = Article.objects.filter(user=request.user)

    context = {'AllArticles': articles}
    return render(request, 'writer/my-articles.html', context)



@login_required(login_url='my-login')
def update_article(request, pk):

    try:
        article = Article.objects.get(id=pk, user=request.user)
    except Article.DoesNotExist:
        return redirect('my-articles')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            form.save()

            # handle new uploaded images
            files = request.FILES.getlist('images')
            if files:
                for file in files:
                    ArticleImage.objects.create(article=article, image=file)

            return redirect('my-articles')

    else:
        form = ArticleForm(instance=article)

    context = {
        'UpdateArticleForm': form,
        'article': article
    }

    return render(request, 'writer/update-article.html', context)



@login_required(login_url='my-login')
def delete_article(request, pk):

    try:
        article = Article.objects.get(id=pk, user=request.user)
    except Article.DoesNotExist:
        return redirect('my-articles')

    if request.method == 'POST':
        article.delete()
        return redirect('my-articles')

    return render(request, 'writer/delete-article.html')



@login_required(login_url='my-login')
def delete_image(request, pk):

    try:
        image = ArticleImage.objects.get(id=pk, article__user=request.user)
        article_id = image.article.id
        image.delete()

        return redirect('update-article', pk=article_id)

    except ArticleImage.DoesNotExist:
        return redirect('my-articles')



@login_required(login_url='my-login')
def account_management(request):

    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')

    context = {'UpdateUserForm': form}
    return render(request, 'writer/account-management.html', context)