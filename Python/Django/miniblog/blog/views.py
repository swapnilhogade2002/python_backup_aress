from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from.forms import SignUpForms,LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group

# home
def home(request):
  posts = Post.objects.all()
  return render(request,'blog/home.html',{'posts':posts})

# about
def about(request):
  return render(request,'blog/about.html')

# contact
def contact(request):
  return render(request,'blog/contact.html')

# dashboard
def dashboard(request):
  if request.user.is_authenticated:
    posts=Post.objects.all()
    user=request.user
    full_name=user.get_full_name()
    gps=user.groups.all()
    return render(request,'blog/dashboard.html',
                  {'posts':posts,'user':user, 'full_name':full_name,'gps':gps})
  else:
    return HttpResponseRedirect('/login/')

#logout
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')

#signup
def user_signup(request):
  if request.method=="POST":
    form=SignUpForms(request.POST)
    if form.is_valid():
      messages.success(request,'Congratulation, you become author !!!')
      user=form.save()
      group=Group.objects.get(name='Author')
      user.groups.add(group)
  else: 
    form=SignUpForms()
  return render(request, 'blog/signup.html',{'form':form})

#login
def user_login(request):
  if not request.user.is_authenticated:
    if request.method=="POST":
      form=LoginForm(request=request, data=request.POST)
      if form.is_valid():
        uname=form.cleaned_data['username']
        upass=form.cleaned_data['password']
        user=authenticate(username=uname, password=upass)
        if user is not None:
          login(request,user)
          messages.success(request,'login successfully !')
          return HttpResponseRedirect('/dashboard/')
    else:   
      form=LoginForm()
    return render(request, 'blog/login.html',{'form':form})
  else:
    return HttpResponseRedirect('/dashboard/')



#add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)  # Corrected from request.method.POST to request.POST
            if form.is_valid():
                form.save()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

#add update post
def update_post(request,id):
  if request.user.is_authenticated:
    if request.method=='POST':
      pi=Post.objects.get(pk=id)
      form=PostForm(request.POST, instance=pi)
      if form.is_valid():
        form.save()
    else:
      pi=Post.objects.get(pk=id)
      form=PostForm(instance=pi)
    return render(request,'blog/updatepost.html',{'form':form})
  else:
    return HttpResponseRedirect('/login/')
  
  
#delete post

def delete_post(request,id):
  if request.user.is_authenticated:
    if request.method=='POST':
      post=Post.objects.get(pk=id)
      post.delete()
      return HttpResponseRedirect('/dashboard/')
  else:
    return HttpResponseRedirect('/login/')
  
  # pi=Post.objects.get(pk=id)
  # pi.delete()
  # return HttpResponseRedirect('/')