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

