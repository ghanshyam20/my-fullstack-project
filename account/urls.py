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
    path('profile/', views.profile_page, name='profile-page'),
    path('apply-writer/', views.apply_writer, name='apply-writer'),
    path('writer-pending/', views.writer_pending, name='writer-pending'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-verify/<int:user_id>/', views.verify_reset_otp, name='reset-verify'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset-password'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('delete-account/', views.delete_account, name='delete-account'),

    ]