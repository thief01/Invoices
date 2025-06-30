from django.urls import path
from . import views

urlpatterns =[
    path('add', views.add_new_compoany, name='add'),
    path('get', views.get_companies, name='get_companies'),
]
