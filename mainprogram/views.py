from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'mainprogram/home.html')

def profile(request):
    return render(request, 'mainprogram/profile.html')

def login(request):
    return render(request, 'mainprogram/login.html')

def register(request):
    return render(request, 'mainprogram/register.html')

def add_account(request):
    return render(request, 'mainprogram/add_account.html')

def logout(request):
    auth_logout(request)
    return redirect('login')