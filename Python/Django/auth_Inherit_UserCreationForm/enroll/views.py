from django.shortcuts import render
from .forms import SignUpForm
# Create your views here.
def sign_up(request):
  if request.method=="POST":
    fm=SignUpForm(request.POST)
    if fm.is_valid():
      fm.save()
  else:
    fm=SignUpForm()
  return render(request,'enroll/signup.html',{'form':fm})