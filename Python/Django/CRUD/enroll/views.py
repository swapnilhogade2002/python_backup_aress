from django.shortcuts import render,HttpResponseRedirect
from .forms import StudentRegistrations
from .models import User
# Create your views here.

#show data on a page
def add_show(request):
  if request.method=='POST':
    fm=StudentRegistrations(request.POST)
    if fm.is_valid():
      fm.save()
      fm=StudentRegistrations()
  else:
    fm=StudentRegistrations()
    
  stud=User.objects.all()
  return render(request,'enroll/addandshow.html',{'form':fm,'stud':stud})

#update data
def update_data(request,id):
  if request.method=='POST': 
    pi=User.objects.get(pk=id)
    fm=StudentRegistrations(request.POST, instance=pi)
    if fm.is_valid():
      fm.save()
  else:
    pi=User.objects.get(pk=id)
    fm=StudentRegistrations(instance=pi)
  return render(request,'enroll/update.html',{'form':fm})

# delete data
def delete_data(request,id):
  if request.method=='POST':
    pi=User.objects.get(pk=id)
    pi.delete()
    return HttpResponseRedirect('/')