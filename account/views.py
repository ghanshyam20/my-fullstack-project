from django.shortcuts import render

from .forms import CreateUserForm
from django.http import HttpResponse



def home(request):
    return render(request,'account/index.html')



def register(request):


    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('user registered')
        

    context={'RegisterForm':form}

    return render(request, 'account/register.html',context)










def my_login(request):
    return render(request,'account/my-login.html')



