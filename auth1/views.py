from django.shortcuts import render


def home(request):
    return render(request, 'auth1/home.html')

def profile(request):
    data = {
        'nickname': 'RaR'
    }
    return render(request, 'auth1/profile.html', data)

def auth(request):
    return render(request, 'auth1/auth.html')

def logout(request):
    return render(request, 'auth1/auth.html')
