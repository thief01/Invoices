import json

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
        login(request, user)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)



def user_logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def user_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=409)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)