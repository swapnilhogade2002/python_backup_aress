from django.shortcuts import render ,HttpResponseRedirect
from .forms import SignUpForm,EditUserProfile,EditAdminProfile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm,SetPasswordForm,UserChangeForm 
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib import messages
from django.forms.utils import ErrorDict
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
import logging

# Create your views here.
def sign_up(request):
  if request.method=="POST":
    fm=SignUpForm(request.POST)
    if fm.is_valid():
      fm.save()
      messages.success(request,"registerd successfully !!!!")
  else:
    fm=SignUpForm()
    
  return render(request,'enroll/signup.html',{'form':fm})

#user login
def user_login(request):
  # if not request.user.is_authenticated:
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
  # else:
  #   return HttpResponseRedirect('/profile/')


#user profile
#user profile
def user_profile(request):
    users = None  # Initialize users variable
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser == True:
                fm = EditAdminProfile(request.POST, instance=request.user)
                users = User.objects.all()  # Set users variable if user is a superuser
            else:
                fm = EditUserProfile(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Profile is updated successfully!')
        else:
            if request.user.is_superuser == True:
                fm = EditAdminProfile(instance=request.user)
                users = User.objects.all()  # Set users variable if user is a superuser
            else:
                fm = EditUserProfile(instance=request.user)
    else:
        return HttpResponseRedirect('/signup/')
    
    return render(request, 'enroll/profile.html', {
        "name": request.user,
        "form": fm,
        'users': users  # Pass users variable to the template
    })


#user logout
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/signup/')

logger = logging.getLogger(__name__)

# Change password with old password
def user_change_pass(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      fm = PasswordChangeForm(user=request.user, data=request.POST)
      if fm.is_valid():
        fm.save()
        logger.info("Password changed successfully.")
        update_session_auth_hash(request, request.user)  # Update session auth hash
        return HttpResponseRedirect('/profile/')
      else:
        logger.error("Form validation failed: %s", fm.errors)
        return HttpResponseServerError("Form validation failed. Please check the form data.")
    else:
      fm = PasswordChangeForm(user=request.user)
    return render(request, 'enroll/change_password.html', {'form': fm})
  else:
    return HttpResponseRedirect('/login/')
  
  # Change password withoute old password
def user_change_pass(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      fm = SetPasswordForm(user=request.user, data=request.POST)
      if fm.is_valid():
        fm.save()
        logger.info("Password changed successfully.")
        update_session_auth_hash(request, request.user)  # Update session auth hash
        return HttpResponseRedirect('/profile/')
      else:
        logger.error("Form validation failed: %s", fm.errors)
        return HttpResponseServerError("Form validation failed. Please check the form data.")
    else:
      fm = SetPasswordForm(user=request.user)
    return render(request, 'enroll/change_password1.html', {'form': fm})
  else:
    return HttpResponseRedirect('/login/')
  
  
def user_detail(request,id):
  if request.user.is_authenticated:
    pi=User.objects.get(pk=id)
    fm=EditAdminProfile(instance=pi)
    return render(request,'enroll/userdetail.html',{'form':fm})
  else:
    return HttpResponseRedirect('/login/')