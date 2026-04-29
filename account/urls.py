from django.urls import path
from . import views




urlpatterns=[
    path('', views.home,name=""),
    path('register', views.register, name='register'),
    path('my-login/', views.my_login, name='my-login'),
    path('user-logout', views.user_logout, name="user-logout"),
    path('verify/<int:user_id>/', views.verify_otp, name='verify-otp'),
    path('terms/',views.terms,name='terms'),
    path('privacy/',views.privacy,name="privacy"),
    path('export-data/', views.export_data, name='export-data'),
    path('settings/', views.account_settings, name='account-settings'),
    path('apply-writer/', views.apply_writer, name='apply-writer'),
    path('writer-pending/', views.writer_pending, name='writer-pending'),
    



]