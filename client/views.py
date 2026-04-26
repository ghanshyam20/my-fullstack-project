from django.shortcuts import get_object_or_404, redirect, render
from client.models import Article, Like ,Comment,Bookmark,Report
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

#for the client 

#decorators 

@login_required(login_url='my-login')
def client_dashboard(request):
    articles=Article.objects.all()
    return render (request, 'client/client-dashboard.html',{
        'articles':articles
    })





@login_required(login_url='my-login')
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments=Comment.objects.filter(article=article).order_by('-date_posted')

    is_bookmarked=Bookmark.objects.filter(
        user=request.user,
        article=article 
    )

    return render(request, 'client/article_detail.html', {
        'article': article,
        'comments': comments,
        'is_bookmarked': is_bookmarked
    })






@login_required
def toggle_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    like = Like.objects.filter(
        user=request.user,
        article=article
    )

    if like.exists():
        like.delete()
        liked = False
    else:
        Like.objects.create(
            user=request.user,
            article=article
        )
        liked = True

    total_likes = Like.objects.filter(article=article).count()

    return JsonResponse({
        'liked': liked,
        'total_likes': total_likes
    })





from .models import Comment

@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                user=request.user,
                article=article,
                content=content
            )

    return redirect('article-detail', id=article.id)




@login_required
def toggle_bookmark(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        article=article
    )

    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True

    total_bookmarks = Bookmark.objects.filter(article=article).count()

    return JsonResponse({
        'bookmarked': bookmarked,
        'total_bookmarks': total_bookmarks
    })



@login_required
def report_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        reason = request.POST.get('reason')

        report, created = Report.objects.get_or_create(
            user=request.user,
            article=article,
            defaults={'reason': reason}
        )

        if not created:
            return JsonResponse({
                'status': 'already_reported'
            })

        return JsonResponse({
            'status': 'reported'
        })