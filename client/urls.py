from django.urls import path 
from . import views



urlpatterns=[
    path('client-dashboard',views.client_dashboard,name="client-dashboard"),
    #path('account-management',views.account_management,name="acco()
    path('article/<int:id>/', views.article_detail, name='article-detail'),

]