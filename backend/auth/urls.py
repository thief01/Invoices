from django.urls import path
from . import views

urlpatterns =[
    path('login', views.login_post, name='login'),
    path('register', views.register_post, name='register'),
    path('logout', views.logout_post, name='logout'),
]
