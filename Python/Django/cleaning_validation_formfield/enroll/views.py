from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import StudentRegistration
# Create your views here.

#for success page
def thanks(request):
    return render(request,'enroll/success.html')
    
def showFormData(request):
    if request.method == 'POST':
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            print("form valid request")
            name=fm.cleaned_data['name']
            print("Name",name)
            return HttpResponseRedirect('/form/success')
            #for same page
            # return render(request, 'enroll/success.html', {'nm': name})
    else:
        fm = StudentRegistration() 
    
    return render(request, 'enroll/regform.html', {'form': fm})
  