from django.db import IntegrityError
import requests
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from client.models import Article, Like ,Comment,Bookmark, Notification,Report
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from client.models import Subscription
from django.db.models import Q, Case, When, IntegerField
from client.models import ArticleView
from django.db import transaction
from client.models import Payment

from django.db.models import Count 
import logging
logger = logging.getLogger(__name__)




def is_writer_only(request):
    return request.user.is_writer and not request.user.is_staff

def is_client_only(request):
    return not request.user.is_writer and not request.user.is_staff


#for the client 

#decorators 





def get_paypal_token():
    try:
        url=f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"
        response = requests.post(
            url,
            auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
            data={"grant_type": "client_credentials"},
            timeout=5
        )

        response.raise_for_status()  # will raise an error for bad status codes

        data=response.json()

        if "access_token" not in data:
            logger.error(f"Invalid PayPal token response: {data}")
            return None
        return data.get('access_token')
    
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return None


@login_required(login_url='my-login')
def client_dashboard(request):
    if is_writer_only(request):
        return redirect('writer-dashboard')
    query = request.GET.get('q', '').strip()
    filter_type=request.GET.get('type')

    articles = Article.objects.select_related('user') \
        .prefetch_related('images', 'article_likes', 'article_bookmarks', 'article_views') \
        .annotate(
            total_likes=Count('article_likes', distinct=True),
            total_bookmarks=Count('article_bookmarks', distinct=True),
            total_views=Count('article_views', distinct=True)
    ).filter(is_published=True)


    if filter_type =='free':
        articles = articles.filter(is_premium=False)
    elif filter_type == 'premium':
        articles = articles.filter(is_premium=True)

    
   

   

  



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
    if is_writer_only(request):
        return redirect('writer-dashboard')
    
   
    article = get_object_or_404(
        Article.objects.annotate(
            total_likes=Count('article_likes', distinct=True),
            total_bookmarks=Count('article_bookmarks', distinct=True),
            total_views=Count('article_views', distinct=True)
        ),
        id=id,
        is_published=True
    )

    # i have added view track  for recetn view and count as view new


    recent_view=ArticleView.objects.filter(
        user=request.user,
        article=article,
        viewed_at__gte=timezone.now() - timedelta(minutes=2)
        
        ).exists()
    
    if not recent_view:
        ArticleView.objects.create(
            user=request.user,
            article=article
        )

    # this wrill refetch new update 


   

    total_likes=article.total_likes
    total_bookmarks=article.total_bookmarks
    total_views=article.total_views


    comments=Comment.objects.filter(
        article=article,
        parent=None
        ).select_related('user').prefetch_related('replies__user').order_by('-date_posted')
    

    is_bookmarked=Bookmark.objects.filter(
        user=request.user,
        article=article
    ).exists()


    subscription=getattr(request.user, 'subscription', None)

    can_access=True
    



    if article.is_premium and not request.user.is_staff:
        if not subscription or not subscription.is_valid():
            can_access=False

       
    
    


    return render(request, 'client/article_detail.html', {
        'article': article,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
        'can_access': can_access,
        'total_likes': total_likes,
        'total_bookmarks': total_bookmarks,
        'total_views': total_views,
        })




    

      


   


    

@login_required
@require_POST
def toggle_like(request, article_id):
    if is_writer_only(request):
        return JsonResponse({"error": "Access denied."}, status=403)
    article = get_object_or_404(Article, id=article_id)

    try:
        Like.objects.create(
            user=request.user,
            article=article
        )
        liked=True

        if article.user != request.user:
            Notification.objects.create(
            user=article.user,
            message=f"{request.user.first_name or request.user.email} liked your article",
            link=f"/client/article/{article.id}/",
            type="LIKE"
        )



    except IntegrityError:
        Like.objects.filter(
            user=request.user,
            article=article
        ).delete()
        liked=False 

   

   

    total_likes = Like.objects.filter(article=article).count()

    return JsonResponse({
        'liked': liked,
        'total_likes': total_likes
    })






@login_required
@require_POST
def add_comment(request, article_id):
    if is_writer_only(request):
        return redirect('writer-dashboard')
    article = get_object_or_404(Article, id=article_id)

    content = request.POST.get('content', '').strip()

    if content and len(content)>2:
            Comment.objects.create(
                user=request.user,
                article=article,
                content=content
            )


            if article.user != request.user:
                Notification.objects.create(
                    user=article.user,
                    message=f"{request.user.first_name or request.user.email} commented on your article",
                    link=f"/client/article/{article.id}/",
                    type="COMMENT"
                )
            messages.success(request, "Comment added successfully.")

    else:
        messages.error(request, "Comment must be at least 3 characters long.")

    return redirect('article-detail', id=article.id)


@login_required
def delete_comment(request, comment_id):
    if is_writer_only(request):
        return redirect('writer-dashboard')

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
    if is_writer_only(request):
        return JsonResponse({"error": "Access denied."}, status=403)

    comment= get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({
            "success": False,
            "error": "Unauthorized"
        }, status=403)
    

    new_content = request.POST.get('content',"").strip()

    if not new_content or len(new_content)<3:
        return JsonResponse({
            "success": False,
            "error": "Content must be at least 3 characters long"
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
    if is_writer_only(request):
        return JsonResponse({"error": "Access denied."}, status=403)
    article = get_object_or_404(Article, id=article_id)

    try:
        Bookmark.objects.create(
            user=request.user,
            article=article
        )
        bookmarked=True

    except IntegrityError:
        Bookmark.objects.filter(
            user=request.user,
            article=article
        ).delete()
        bookmarked=False


    total = Bookmark.objects.filter(article=article).count()

    return JsonResponse({
        "bookmarked": bookmarked,
        "total_bookmarks": total
    })

 


  

    


    
   

@login_required
@require_POST
def report_article(request, article_id):
    if is_writer_only(request):
        return JsonResponse({"error": "Access denied."}, status=403)
    article = get_object_or_404(Article, id=article_id)

    
    reason = request.POST.get('reason','').strip()
    if not reason:
        return JsonResponse({
            'status': 'error',
            'message': 'Reason is required.'
        }, status=400)      

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
    if is_writer_only(request):
        return redirect('writer-dashboard')
        
    
    next_url = request.GET.get('next')

    return render(request, 'client/subscription.html', {'next_url': next_url})



@login_required
def create_paypal_order(request):
    if is_writer_only(request):
        return redirect('writer-dashboard')

    token = get_paypal_token()
    if not token:
        messages.error(request, "Unable to connect to payment gateway.")
        return redirect('client-dashboard')

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
            "return_url": f"{settings.SITE_URL}/client/payment-success/?next={next_url}",
            "cancel_url": f"{settings.SITE_URL}/client/payment-cancel/"
        }
    }

    response = requests.post(
        url,
        json=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        timeout=5
    )

    if response.status_code not in [200, 201]:
        messages.error(request, "Payment service error. Please try again later.")
        return redirect('client-dashboard')


    

 
    
        

    order = response.json()

    #  redirect user to paypal  approval url 
    for link in order.get('links', []):
        if link.get('rel') == 'approve':
            return redirect(link.get('href'))
        
    messages.error(request, "Unable to redirect to PayPal.")
    return redirect('client-dashboard')
        

        



@login_required
def payment_success(request):
    if is_writer_only(request):
        return redirect('writer-dashboard')

    order_id = request.GET.get("token")
    next_url = request.GET.get("next", "client-dashboard")

    if not order_id:
        messages.error(request, "Missing PayPal token.")
        return redirect('client-dashboard')
    


    if Payment.objects.filter(paypal_order_id=order_id, status="COMPLETED").exists():
        messages.warning(request, "payment  has already been processed.")
        return redirect(next_url)
    



    data=None

    try:
        token = get_paypal_token()
        if not token:
            messages.error(request, "payment service unavailable.")
            return redirect('client-dashboard')

        url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=5
        )

        if response.status_code not in [200, 201]:
            messages.error(request, "Payment capture failed. Please try again.")
            return redirect('client-dashboard')

       

        data = response.json()

        try:
            amount_paid = data["purchase_units"][0]["payments"]["captures"][0]["amount"]["value"]
            currency = data["purchase_units"][0]["payments"]["captures"][0]["amount"]["currency_code"]
        except (KeyError, IndexError):
            logger.error(f"Invalid PayPal structure: {data}")
            messages.error(request, "Invalid payment data.")
            return redirect('client-dashboard')


        if currency != "USD":
            messages.error(request, "Invalid currency.")
            return redirect('client-dashboard')

     
        

        try:
            if  round(float(amount_paid), 2) != 4.99:
                messages.error(request, "Invalid payment amount.")
                return redirect('client-dashboard')
        except ValueError:
                messages.error(request, "Invalid payment format.")
                return redirect('client-dashboard')

       

       
        


        #print("PAYPAL RESPONSE:", data)
        if data.get("id")!= order_id:
            messages.error(request, "Order ID mismatch.")
            return redirect('client-dashboard')
        

        payer=data.get("payer")
        if not payer:
            messages.error(request,"Invalid payer")
            return redirect('client-dashboard')
        
        payer_email=payer.get("email_address")

        if not payer_email:
            messages.error(request,"Payer email not found.")
            return redirect('client-dashboard')

    except requests.Timeout:
        messages.error(request, "Payment timeout. Try again.")
        return redirect('client-dashboard')

    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
        messages.error(request, "Payment processing failed.")
        return redirect('client-dashboard')
    

    if not data:
        messages.error(request, "Invalid payment data received.")
        return redirect('client-dashboard')
    

    capture_status=(
        data.get("purchase_units", [{}])[0]
        .get("payments", {})
        .get("captures", [{}])[0]
        .get("status","")

    )
    

    if not capture_status:
        messages.error(request, "Payment status not found.")
        return redirect('client-dashboard')
   

    payment_completed =(
        data.get("status") == "COMPLETED" and
        capture_status.upper() == "COMPLETED"
        )

    
       

    if payment_completed:
        with transaction.atomic():
            if Payment.objects.select_for_update().filter(paypal_order_id=order_id).exists():
                return redirect(next_url)

            sub, _ = Subscription.objects.get_or_create(user=request.user)

      
            sub.plan = "PREMIUM"
            sub.is_active = True
            sub.cost = 4.99

            if sub.expires_at and sub.expires_at > timezone.now():
                sub.expires_at += timedelta(days=30)
            else:
                sub.expires_at = timezone.now() + timedelta(days=30)
            sub.save()
            logger.info(f"Subscription updated: user={request.user.id}, expires={sub.expires_at}")

            Payment.objects.get_or_create(
                paypal_order_id=order_id,
                defaults={
                "user": request.user,
                "subscription": sub,
                "status": "COMPLETED",
                "amount": sub.cost,
                "payer_email": payer_email
                }
            )
            
        #notify user
        

            Notification.objects.create(
                        user=request.user,
                        message="Your Premium subscription is now active. Enjoy our exclusive Tech content!",
                        type="PAYMENT"
            )
            
            messages.success(request, "Payment successful! Premium unlocked.")

            logger.info(
            f"Payment SUCCESS: user={request.user.id}, order={order_id},email={payer_email}"
            )


    
        

        try:
            send_mail(
                subject="Your Premium Subscription is Activated",
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
            logger.error(f"Error sending email: {str(e)}")
            messages.error(request, "Failed to send confirmation email.")


    #  handle response and activate subscription if payment completed
   

        #email send 
        
                
                    
               
             

    else:
        amount=4.99
        Payment.objects.get_or_create(
            paypal_order_id=order_id,
            defaults={
                "user": request.user,
                "subscription": None,
                "status": "FAILED",
                "amount": amount
            }
        )
        logger.warning(f"Payment not completed for order {order_id}. Response: {data}")
        messages.error(request, "Payment not completed.")

    return redirect(next_url or 'client-dashboard')


@login_required
def payment_cancel(request):
    messages.warning(request, "Payment cancelled.")
    return redirect('client-dashboard')