from django.shortcuts import render
from .forms import UserRegistration
# Create your views here.
def showformdata(request):
  fm=UserRegistration()
  return render(request,'enroll/userregister.html',{'form':fm})
  