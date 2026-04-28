from django.urls import path
from . import views




urlpatterns=[
    path('', views.home,name=""),
    path('register', views.register, name='register'),
    path('my-login', views.my_login, name='my-login'),
    path('user-logout', views.user_logout, name="user-logout"),
    path('verify/<int:user_id>/', views.verify_otp, name='verify-otp'),
    path('terms/',views.terms,name='terms'),
    path('privacy/',views.privacy,name="privacy"),
    



]