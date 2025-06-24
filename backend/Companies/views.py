import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, JsonResponse

from Companies.models import Company


@login_required
def add_new_compoany(request):
    if request.method == "POST":
        company = Company()
        data = json.loads(request.body)
        company.name = data.get('name')
        company.vat = data.get('vat')
        company.tax_value = data.get('tax_value', 12)
        company.company_type = data.get('company_type')
        company.user = request.user
        try:
            company.clean()
            company.save()
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'errors': e.message_dict})
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

