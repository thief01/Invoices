from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, JsonResponse

from Companies.models import Company


def add_new_compoany(request):
    if request.method == "POST":
        company = Company()
        company.name = request.POST['name']
        company.vat = request.POST['vat']
        company.tax_value = request.POST['tax_value']
        company.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def get_companies(request):
    if request.method == "GET":
        companies =  Company.objects.filter(user = request.user)
        return JsonResponse({
            'status': 'success',
            'companies': list(companies.values('id', 'name', 'vat', 'tax_value', 'company_type'))
        })
    return JsonResponse({'status': 'error'})

