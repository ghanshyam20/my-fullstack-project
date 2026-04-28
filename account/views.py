import random
from django.shortcuts import render , redirect
from django.core.mail import send_mail
from .forms import CreateUserForm
from .models import EmailOtp, CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login, logout



def home(request):
    return render(request,'account/index.html')



def register(request):


    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)

            user.set_password(form.cleaned_data['password1'])

            user.is_active=False

            user.consent_given=form.cleaned_data['consent']
            user.save()


            otp_code=str(random.randint(100000,999999))

            EmailOtp.objects.update_or_create(
                user=user,
                defaults={'otp': otp_code}
            )


            send_mail(
                subject="Your OPT CODE",
                message=f"Your OTP code is {otp_code}",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return redirect('verify-otp',user_id=user.id)
        

    context={'RegisterForm':form}


    return render(request, 'account/register.html',context)
    

def verify_otp(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    otp_obj=EmailOtp.objects.get(user=user)


    if request.method=='POST':
        entered_otp=request.POST.get('otp')


        if otp_obj.otp==entered_otp and otp_obj.is_valid():
            user.is_active=True
            user.save()
            otp_obj.delete()
            return redirect('my-login')
        


    return render(request,'account/verify.html',{'user':user})
         










def my_login(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None and user.is_active:

                if user.is_writer:

                    login(request,user)
                    return redirect('writer-dashboard')
                
                else:
                    login(request,user)
                    return redirect('client-dashboard')
                    
            

            
            

    context={'LoginForm':form}
    return render(request,'account/my-login.html',context)




def user_logout(request):
    logout(request)
    return redirect("my-login")








