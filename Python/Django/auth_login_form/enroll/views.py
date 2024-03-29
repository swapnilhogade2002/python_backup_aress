from django.shortcuts import render ,HttpResponseRedirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages


# Create your views here.
def sign_up(request):
  if request.method=="POST":
    fm=SignUpForm(request.POST)
    if fm.is_valid():
      fm.save()
  else:
    fm=SignUpForm()
  return render(request,'enroll/signup.html',{'form':fm})

#user login
def user_login(request):
  if not request.user.is_authenticated:
    if request.method=="POST":
      fm=AuthenticationForm(request=request,data=request.POST)
      if fm.is_valid():
        uname=fm.cleaned_data['username']
        upass=fm.cleaned_data['password']
        user=authenticate(username=uname,password=upass)
        if user is not None:
          login(request, user)
          messages.success(request,'login succesfully!')
          return HttpResponseRedirect('/profile/')
    else:
      fm=AuthenticationForm()
      return render(request,'enroll/login.html',{'form':fm})
  else:
    return HttpResponseRedirect('/profile/')


#user profile
def user_profile(request):
  if request.user.is_authenticated:
    return render(request,'enroll/profile.html',{"name":request.user})
  else:
    return HttpResponseRedirect('/signup/')

#user logout
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/signup/')