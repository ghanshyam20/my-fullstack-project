from django.urls import path 


from . import views


urlpatterns=[
    path('', views.writer_home, name='writer_home'),
]