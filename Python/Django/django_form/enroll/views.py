from django.shortcuts import render
from .forms import StudentRegistration
# Create your views here.

def showFormData(request):
  fm=StudentRegistration()
  return render(request,'enroll/regform.html',{'form':fm})
  