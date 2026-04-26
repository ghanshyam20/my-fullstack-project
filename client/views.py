from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render
from client.models import Article, Like ,Comment,Bookmark,Report
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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
    ).exists()


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
            messages.success(request, "Comment added successfully.")

    return redirect('article-detail', id=article.id)


@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    # security: only owner can delete
    if comment.user != request.user:
        return redirect('article-detail', id=comment.article.id)

    article_id = comment.article.id
    comment.delete()

    messages.success(request, "Comment deleted successfully.")
    return redirect('article-detail', id=article_id)


@login_required
@require_POST

def edit_comment(request, comment_id):

    comment= get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({
            "success": False,
            "error": "Unauthorized"
        }, status=403)
    

    new_content = request.POST.get('content',"").strip()

    if not new_content:
        return JsonResponse({
            "success": False,
            "error": "Content cannot be empty"
        }, status=400)
    
    comment.content = new_content
    comment.save()

    return JsonResponse({
        "success": True,
        "content": comment.content,
        "comment_id": comment.id
    })
    



@login_required
@require_POST
def toggle_bookmark(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    existing = Bookmark.objects.filter(
        user=request.user,
        article=article
    )

    if existing.exists():
        existing.delete()
        bookmarked = False
    else:
        Bookmark.objects.create(
            user=request.user,
            article=article
        )
        bookmarked = True

    total = Bookmark.objects.filter(article=article).count()

    return JsonResponse({
        "bookmarked": bookmarked,
        "total_bookmarks": total
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