from django.shortcuts import render
from .forms import UserRegistrations
from django.contrib import messages
# Create your views here.
def register(request):
  if request.method=='POST':
    fm=UserRegistrations(request.POST)
    if fm.is_valid():
      fm.save()
      fm=UserRegistrations()
      messages.add_message(request,messages.SUCCESS,'Your account has been created')
      messages.info(request,'than you!')
      
  else:
    fm=UserRegistrations()
  return render(request,'enroll/register.html',{'form':fm} )
      