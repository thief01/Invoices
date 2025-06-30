from django.urls import path
from . import views

urlpatterns =[
    path('add', views.add_new_company, name='add_new_company'),
    path('delete_company/<int:company_id>', views.delete_company, name='delete_company'),
    path('company_detail/<int:company_id>/', views.company_detail, name='company_detail'),
    path('edit_company/<int:company_id>/', views.edit_company, name='edit_company'),
    path('get', views.get_companies, name='get_companies'),
]
