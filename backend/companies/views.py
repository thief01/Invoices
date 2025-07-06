import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.


from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from companies.forms import CompanyForm
from companies.models import Company
from invoices.models import CostInvoice, RevenueInvoice


@login_required
def companies_list(request):
    messages.success(request, 'Companies List')
    companies = Company.objects.all()
    if request.method == "GET":
        companies =  Company.objects.filter(user = request.user)
        return render(request, 'companies/companies-list.html', {'companies': companies})
    return JsonResponse({'status': 'Method not allowed'}, status=405)


@login_required
def add_new_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        company = form.save(commit=False)
        company.user = request.user
        company.save()
        messages.success(request, 'Company added successfully')
        return redirect("get_companies")
    else:
        form = CompanyForm(initial={'user': request.user})
    return render(request, 'companies/create-company.html', {'form': form})



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
def company_details(request, company_id):
    company = Company.objects.filter(id=company_id, user=request.user).first()
    cost_invoices = CostInvoice.objects.filter(company = company)
    revenue_invoices = RevenueInvoice.objects.filter(company = company)
    if company:
        return render(request, 'companies/company-details.html', {'company': company})
    else:
        messages.error(request, 'Company not found')
        return redirect('get_companies')
    return JsonResponse({'status': 'Method not allowed'}, status=405)

@login_required
def edit_company(request, company_id):
    return JsonResponse({'status': 'Method not allowed'}, status=405)