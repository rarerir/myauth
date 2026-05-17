from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def home(request):
    return render(request, 'mainprogram/home.html')

def profile(request):
    return render(request, 'mainprogram/profile.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'mainprogram/login.html', {'form': form})

def register(request):
    error = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error = 'Форма неверна'
    else:
        form = RegisterForm()

    return render(request, 'mainprogram/register.html', {'form': form, 'error': error})

def add_account(request):
    return render(request, 'mainprogram/add_account.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def deactivate_user(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        logout(request)

    return redirect('profile')
