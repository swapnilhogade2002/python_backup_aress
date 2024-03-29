from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import StudentRegistration
from .models import User
# Create your views here.

#for success page
def thanks(request):
    return render(request,'enroll/success.html')
    
def showFormData(request):
    if request.method == 'POST':
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            name=fm.cleaned_data['name']
            email=fm.cleaned_data['email']
            password=fm.cleaned_data['password']
    else:
        fm = StudentRegistration() 
    
    return render(request, 'enroll/regform.html', {'form': fm})
  