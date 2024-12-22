from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, 'Your account has been created successfully!')
            return redirect('shop:home')  # Redirect to the home page or any other page
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log in the user
            login(request, user)
            messages.success(request, 'login was successful!')
            return redirect('shop:home')  # Redirect to a success page
        else:
            # Invalid login credentials
            messages.error(request,'Invalid Credentials')
            return render(request, 'login.html')
    return render(request, 'registration/login.html')