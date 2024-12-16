from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
