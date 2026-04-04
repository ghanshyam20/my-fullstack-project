from django.shortcuts import render



def home(request):
    return render(request,'account/index.html')



def register(request):
    return render(request, 'account/register.html')


def my_login(request):
    return render(request,'account/my-login.html')



