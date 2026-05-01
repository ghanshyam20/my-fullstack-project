import requests
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from client.models import Article, Like ,Comment,Bookmark,Report
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from client.models import Subscription
from django.shortcuts import render
from django.db.models import Q, Case, When, IntegerField


#for the client 

#decorators 





def get_paypal_token():
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"

    response = requests.post(
        url,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
        data={"grant_type": "client_credentials"}
    )

    return response.json()['access_token']


@login_required(login_url='my-login')
def client_dashboard(request):
    query = request.GET.get('q', '').strip()

    articles = Article.objects.all()

    if query:
        terms = query.split()

        q_objects = Q()

        for term in terms:
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(content__icontains=term)

        articles = articles.filter(q_objects).annotate(
            relevance=Case(
                When(title__icontains=query, then=2),
                When(content__icontains=query, then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-relevance', '-date_posted')

    else:
        articles = articles.order_by('-date_posted')

    return render(request, 'client/client-dashboard.html', {
        'articles': articles,
        'query': query
    })





@login_required(login_url='my-login')
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments=Comment.objects.filter(
        article=article,
        parent=None
        ).select_related('user').prefetch_related('replies').order_by('-date_posted')
    

    is_bookmarked=Bookmark.objects.filter(
        user=request.user,
        article=article
    ).exists()


    subscription=getattr(request.user, 'subscription', None)


    if article.is_premium:
        if subscription and subscription.is_valid():
            can_access=True
        else:
            can_access=False
    else:
        can_access=True


    return render(request, 'client/article_detail.html', {
        'article': article,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
        'can_access': can_access
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
    


@login_required
def subscription_page(request):

    # this will block writers
    if request.user.is_writer:
        return redirect('writer-dashboard')
    
    next_url = request.GET.get('next')

    return render(request, 'client/subscription.html', {'next_url': next_url})



@login_required
def create_paypal_order(request):

    token = get_paypal_token()

    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders"

    next_url = request.GET.get("next", "/client/client-dashboard")

    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "4.99"
            }
        }],
        "application_context": {
            "return_url": f"http://127.0.0.1:8000/client/payment-success/?next={next_url}",
            "cancel_url": "http://127.0.0.1:8000/client/payment-cancel/"
        }
    }

    response = requests.post(
        url,
        json=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )

    order = response.json()

    #  redirect user to paypal  approval url 
    for link in order['links']:
        if link['rel'] == 'approve':
            return redirect(link['href'])
        



@login_required
def payment_success(request):

    order_id = request.GET.get("token")
    next_url = request.GET.get("next", "client-dashboard")

    if not order_id:
        messages.error(request, "Missing PayPal token.")
        return redirect('client-dashboard')

    try:
        token = get_paypal_token()

        url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        data = response.json()
        print("PAYPAL RESPONSE:", data)

    except Exception as e:
        print("PAYMENT ERROR:", e)
        messages.error(request, "Payment processing failed.")
        return redirect('client-dashboard')

    #  handle response and activate subscription if payment completed
    payment_completed = (
        data.get("status") == "COMPLETED" or
        data.get("name") == "UNPROCESSABLE_ENTITY"  # already captured
    )

    if payment_completed:

        sub, _ = Subscription.objects.get_or_create(user=request.user)

        #  prevent resetting if already active
        if not sub.is_valid():
            sub.plan = "PREMIUM"
            sub.is_active = True
            sub.cost = 4.99
            sub.expires_at = timezone.now() + timedelta(days=30)
            sub.save()

        # success message
        messages.success(request, " Payment successful! Premium unlocked")

        #email send 
        try:
            send_mail(
                subject=" Your Premium Subscription is Activated ",
                message=(
                        f"Hi {request.user.first_name or 'User'},\n\n"
                        f"Your Premium subscription is now active.\n\n"
                        f"Plan: Premium\n"
                        f"Price: €4.99/month\n"
                        f"Expires on: {sub.expires_at.strftime('%B %d, %Y')}\n\n"
                        f"You now have full access to all premium content.\n\n"
                        f"Thank you for your purchase!\n"
                        f"- InsightHub Team"
                    ),
                
                    
               
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True
            )
        except Exception as e:
            print("EMAIL ERROR:", e)

    else:
        messages.error(request, "Payment not completed.")

    return redirect(next_url)
@login_required
def payment_cancel(request):
    messages.warning(request, "Payment cancelled.")
    return redirect('client-dashboard')