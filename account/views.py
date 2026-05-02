import secrets
import json
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from cms.settings import EMAIL_HOST_USER
from writer.forms import UpdateUserForm
from .forms import CreateUserForm, LoginForm
from .models import EmailOtp, CustomUser
from writer.models import Article
from django.contrib.messages import get_messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'account/index.html')



# this is for registration 

def register(request):

    if request.method=="POST":

        is_writer_request = (
            request.POST.get('writer') == "true" or
            request.POST.get('is_writer') == "true"
        )

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.consent_given = form.cleaned_data['consent_given']

            if is_writer_request:
                user.is_writer_requested = True
                writer_reason=request.POST.get('writer_reason')

                if not writer_reason:
                    messages.error(request,"please tell us why you want to be a writer")
                    return render(request, 'account/register.html', {'RegisterForm': form})
                user.writer_reason = writer_reason



            

            user.save()

            #  for OTP
            otp_code = secrets.randbelow(900000) + 100000
            EmailOtp.objects.filter(user=user).delete()
            EmailOtp.objects.create(user=user, otp=otp_code)

           
            

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
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return redirect('verify-otp', user_id=user.id)

    return render(request, 'account/register.html', {'RegisterForm': form})



# OTP  verification request 

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    otp_obj = EmailOtp.objects.filter(user=user).first()

    if not otp_obj:
        messages.error(request, "No OTP found for this user. Please register again.")
        return redirect('register')
   
    if request.method == 'POST':
        
        entered_otp = request.POST.get('otp').strip()
        print("DB OTP:", otp_obj.otp)
        print("Entered OTP:", entered_otp)
        print("Match", otp_obj.otp == entered_otp)
        print("Is Valid:", otp_obj.is_valid())

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

                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                return redirect('my-login')
            
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
            

    return render(request, 'account/verify.html', {'user': user})
   



            


#  for login 

def my_login(request):
    form=LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)


        if form.is_valid():
            user=form.get_user()
            login(request, user)

            if user.is_writer:
                return redirect('writer-dashboard')
            
            elif user.is_writer_requested:
                return redirect('writer-pending')
            
            else:
                return redirect('client-dashboard')
        else:
            messages.error(request, "Invalid email or password.")

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
def profile_page(request):

    user = request.user

    update_form = UpdateUserForm(instance=user)
    password_form = PasswordChangeForm(user=user)

    # subscription (for both user + writer if exists)
    subscription = None
    try:
        subscription = user.subscription
    except Exception as e:
        logger.error(f"Subscription error:{e}")
        

    if request.method == "POST":

        # update profile
        if "update_profile" in request.POST:
            update_form = UpdateUserForm(request.POST, instance=user)

            if update_form.is_valid():
                update_form.save()
                messages.success(request, "Profile updated")
                return redirect('profile-page')

        # Change password
        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated")
                return redirect('profile-page')

        # update  bio and image
        elif "update_profile_extra" in request.POST:

            profile = user.profile

            profile.bio = request.POST.get("bio")

            if request.FILES.get("profile_picture"):
                profile.profile_picture = request.FILES.get("profile_picture")

            profile.save()
            messages.success(request, "Profile updated")
            return redirect('profile-page')

    return render(request, 'account/profile.html', {
        'UpdateUserForm': update_form,
        'PasswordForm': password_form,
        'subscription': subscription,
    })

   


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

@login_required(login_url='my-login')
def writer_pending(request):
    return render(request, 'account/writer_pending.html')


def forgot_password(request):
    storage=get_messages(request)
    for _ in storage:
        pass
    if request.method == "POST":
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            otp_obj = EmailOtp.objects.filter(user=user).first()

            if otp_obj and otp_obj.is_valid():
                otp_code = otp_obj.otp
            else:
                otp_code = str(secrets.randbelow(900000) + 100000)
                EmailOtp.objects.filter(user=user).delete()
                EmailOtp.objects.create(user=user, otp=otp_code)

            send_mail(
                subject="Reset Your Password - InsightHub",
                message=f"Your OTP is: {otp_code}",
                from_email=None,
                recipient_list=[email],
            )

            return redirect('reset-verify', user_id=user.id)

        messages.success(request, "Check your email for 6-digit code to reset your password.")

    return render(request, 'account/forgot_password.html')

        


        
      



def reset_password(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        return redirect('forgot-password')

    #  protect route
    if request.session.get('reset_verified_user') != user.id:
        return redirect('forgot-password')

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('reset-password', user_id=user.id)

        user.set_password(password1)
        user.save()

        # clear session
        request.session.pop('reset_verified_user', None)

        send_mail(
            subject="Your Password Has Been Updated – InsightHub",
            message=f"Hi {user.first_name},\n\nYour password has been updated successfully.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, "Password updated successfully")
        return redirect('my-login')

    return render(request, 'account/reset_password.html')


def verify_reset_otp(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        return redirect('forgot-password')

    otp_obj = EmailOtp.objects.filter(user=user).first()

    if not otp_obj:
        messages.error(request, "No OTP found.")
        return redirect('forgot-password')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp').strip()

        if otp_obj.otp != entered_otp:
            messages.error(request, "Invalid OTP. Please try again.")

        elif not otp_obj.is_valid():
            messages.error(request, "OTP expired. Request a new one.")

        else:
            otp_obj.delete()
            request.session['reset_verified_user'] = user.id   
            return redirect('reset-password', user_id=user.id)

    return render(request, 'account/verify_reset.html', {'user': user})



    