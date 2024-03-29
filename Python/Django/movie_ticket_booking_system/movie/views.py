from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserForm,TheaterForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .models import User
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
  return render(request,'movie/home.html')

def login(request):
  return render(request,'user/login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request, 'User Registration successful. You can now login.')
          return redirect('/login')
    else:
        form = UserForm()
    return render(request, 'user/register.html', {'form': form})

def create_theater(request):
    if request.method == 'POST':
        form = TheaterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  
    else:
        form = TheaterForm()
    
    return render(request, 'theater/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print("User authenticated:", user)
                return redirect('/home')  # Redirect to the home page after successful login
            else:
                # Handle invalid login
                error_message = "Invalid email or password. Please try again."
                print("Authentication failed for email:", email)
                return render(request, 'user/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})