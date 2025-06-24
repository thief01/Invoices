import json

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


# @csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid username or password'})
        login(request, user)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'})



def user_logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'})

def user_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return JsonResponse({'error': 'Invalid request'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'})