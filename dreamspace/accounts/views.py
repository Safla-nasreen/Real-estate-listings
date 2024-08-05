from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .forms import UserRegistrationForm


def login_user(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            error_message = 'Invalid Username or Password'
    return render(request, 'accounts/login.html', {'error_message': error_message})


def logout_user(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home'))  # Redirect to the home page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})
