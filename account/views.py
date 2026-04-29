import random
import json
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from .forms import CreateUserForm
from .models import EmailOtp, CustomUser
from writer.models import Article


def home(request):
    return render(request, 'account/index.html')



# this is for registration 

def register(request):

    if request.method=="POST":

        is_writer_request = request.POST.get('writer') == "true"
    else:

        is_writer_request = request.GET.get('writer') == "true"

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.consent_given = form.cleaned_data['consent_given']

            if is_writer_request:
                user.is_writer_requested = True

            user.save()

            #  for OTP
            otp_code = str(random.randint(100000, 999999))

            EmailOtp.objects.update_or_create(
                user=user,
                defaults={'otp': otp_code}
            )

            # email message
            if is_writer_request:
                message = (
                    f"Hi {user.first_name},\n\n"
                    "Welcome to InsightHub.\n\n"
                    f"Your OTP code is: {otp_code}\n\n"
                    "You are applying as a writer.\n"
                    "After verification, your request will be reviewed by admin.\n\n"
                    "InsightHub Team"
                )
            else:
                message = (
                    f"Hi {user.first_name},\n\n"
                    "Welcome to InsightHub.\n\n"
                    f"Your OTP code is: {otp_code}\n\n"
                    "use the otp code to continue registration.\n\n"
                    "InsightHub Team"
                )

            send_mail(
                subject="Verify Your Account – InsightHub",
                message=message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return redirect('verify-otp', user_id=user.id)

    return render(request, 'account/register.html', {'RegisterForm': form})



# OTP  verification request 

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    try:
        otp_obj = EmailOtp.objects.get(user=user)
    except EmailOtp.DoesNotExist:
        messages.error(request,"OTP not found.please register again.")
        return redirect('register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if otp_obj.otp == entered_otp and otp_obj.is_valid():
            user.is_active = True
            user.save()
            otp_obj.delete()

            

            #  for writer =  second email + pending page
            if user.is_writer_requested:
                send_mail(
                    subject="Writer Application Received – InsightHub",
                    message=(
                        f"Hi {user.first_name},\n\n"
                        "Your writer application has been submitted.\n\n"
                        "Our admin team will review your request.\n"
                        "You will receive another email once approved.\n\n"
                        "InsightHub Team"
                    ),
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                return redirect('writer-pending')
            

            else:
                login_link="http://localhost:8000/my-login/"

                send_mail(
                    subject="Welcome to InsightHub",
                    message=(
                        f"Hi {user.first_name},\n\n"
                        "your account is ready to use.\n\n"
                        "you can explore our paltform and enjoy reading.\n\n"

                        f"Login here: {login_link}\n\n"
                        "Happy Learning !\n\n"
                        "InsightHub Team"
                    ),

                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                return redirect('my-login')
            
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
            

    return render(request, 'account/verify.html', {'user': user})


            


#  for login 

def my_login(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_writer:
                return redirect('writer-dashboard')

            elif user.is_writer_requested:
                return redirect('writer-pending')

            else:
                return redirect('client-dashboard')

    return render(request, 'account/my-login.html', {'LoginForm': form})


#  for LOGOUT

def user_logout(request):
    logout(request)
    return redirect('my-login')



# for terms 

def terms(request):
    return render(request, 'account/terms.html')


def privacy(request):
    return render(request, 'account/privacy.html')



#  to let the user can Export  Data 

@login_required
def export_data(request):
    user = request.user
    articles = Article.objects.filter(user=user)

    article_list = []
    for article in articles:
        article_list.append({
            "title": article.title,
            "content": article.content,
            "is_premium": article.is_premium,
            "date_posted": str(article.date_posted),
        })

    data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": str(user.date_joined),
        "articles": article_list,
    }

    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="my_data.json"'

    return response



#  for account settings

@login_required
def account_settings(request):
    context = {
        'UpdateUserForm': UpdateUserForm(),
        'PasswordForm': PasswordForm(),
        'subscription': None,
    }
    return render(request, 'account/account_settings.html', context)



# for  APPLY WRITER (logged user )

@login_required(login_url='my-login')
def apply_writer(request):
    user = request.user

    if user.is_writer:
        return redirect('writer-dashboard')

    if user.is_writer_requested:
        return redirect('writer-pending')

    user.is_writer_requested = True
    user.save()

    send_mail(
        subject="Writer Application Received – InsightHub",
        message=(
            f"Hi {user.first_name},\n\n"
            "Your request to become a writer has been submitted.\n\n"
            "Our admin team will review your application.\n\n"
            "InsightHub Team"
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return redirect('writer-pending')


#  for writer waiting pending page 


def writer_pending(request):
    return render(request, 'account/writer_pending.html')