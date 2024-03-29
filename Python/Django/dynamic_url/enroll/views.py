from django.shortcuts import render

# Create your views here.


def home(request):
  return render(request,'enroll/home.html')

# def showDetail(request,my_id ):
#   print(my_id)
#   return render(request,'enroll/show.html',{'id':my_id})

def showDetail(request,my_id ):
  if my_id==1:
    student={'id':my_id, 'name':'swapnil'}
    
  return render(request,'enroll/show.html',student)

def showSubDetail(request,my_id ,my_subid):
  if my_id==1 and my_subid==3:
    student={'id':my_id, 'name':'swapnil'}
    
  return render(request,'enroll/show.html',student)


  
