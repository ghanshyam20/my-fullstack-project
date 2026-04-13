from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#for the client 

#decorators 

@login_required(login_url='my-login')
def client_dashboard(request):
    return render (request, 'client/client-dashboard.html')




