from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def admin_login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_home')
        else:
            error_message = 'Invalid username or password. Please try again.'

    return render(request, 'admin_login.html', {'error_message': error_message})


@login_required
def admin_home(request):
    return render(request, 'admin_home.html')


@login_required
def logout_confirm(request):
    return render(request, 'logout_confirm.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('admin_login')
    return redirect('logout_confirm')