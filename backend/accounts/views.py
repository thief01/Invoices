import json

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Błąd rejestracji. Sprawdź poprawność danych.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})