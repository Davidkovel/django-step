from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('cars:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Ласкаво просимо, {user.first_name}! Реєстрація успішна.')
            return redirect('cars:home')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('cars:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'cars:home')
            messages.success(request, f'Ласкаво просимо, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Невірний логін або пароль.')
    else:
        form = LoginForm(request)

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Ви вийшли з облікового запису.')
    return redirect('cars:home')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})