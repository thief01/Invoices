import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, JsonResponse

from companies.models import Company

@login_required
def get_companies(request):
    if request.method == "GET":
        companies =  Company.objects.filter(user = request.user)
        return render(request, 'companies/companies.html', {'companies': companies})
    return JsonResponse({'status': 'Method not allowed'}, status=405)


@login_required
def add_new_company(request):
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
            return JsonResponse({'status': 'error', 'errors': e.message_dict}, status=400)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'Method not allowed'}, status=405)



@login_required
def update_company(request, company_id):
    if request.method == "POST":
        try:
            company = Company.objects.get(id=company_id, user=request.user)
        except Company.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Company not found'}, status=404)

        data = json.loads(request.body)
        company.name = data.get('name', company.name)
        company.vat = data.get('vat', company.vat)
        company.tax_value = data.get('tax_value', company.tax_value)
        company.company_type = data.get('company_type', company.company_type)

        try:
            company.clean()
            company.save()
            return JsonResponse({'status': 'success'})
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'errors': e.message_dict}, status=400)

    return JsonResponse({'status': 'Method not allowed'}, status=405)


@login_required
def delete_company(request):
    return JsonResponse({'status': 'Method not allowed'}, status=405)

@login_required
def company_detail(request, company_id):
    return JsonResponse({'status': 'Method not allowed'}, status=405)

@login_required
def edit_company(request, company_id):
    return JsonResponse({'status': 'Method not allowed'}, status=405)