from django.urls import path 
from . import views



urlpatterns=[
    path('client-dashboard',views.client_dashboard,name="client-dashboard"),
    #path('account-management',views.account_management,name="account-management"),

]