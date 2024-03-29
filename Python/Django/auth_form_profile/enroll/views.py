from django.shortcuts import render ,HttpResponseRedirect
from .forms import SignUpForm,EditUserProfile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm,SetPasswordForm,UserChangeForm
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib import messages
from django.forms.utils import ErrorDict
from django.http import HttpResponseServerError
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
def user_profile(request):
  if request.user.is_authenticated:
    if request.method=='POST':
      fm=EditUserProfile(request.POST,instance=request.user)
      if fm.is_valid():
        fm.save()
        messages.success(request,'profile is updated succesfully !!!!')
    else:
      fm =EditUserProfile(instance=request.user)
    return render(request,'enroll/profile.html',{"name":request.user , "form":fm})
  else:
    return HttpResponseRedirect('/signup/')

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