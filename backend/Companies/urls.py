from django.urls import path
from . import views

urlpatterns =[
    path('', views.add_new_compoany, name='add'),
]
