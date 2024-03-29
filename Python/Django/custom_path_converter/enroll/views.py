from django.shortcuts import render

# Create your views here.


def home(request):
  return render(request,'enroll/home.html')

# def showDetail(request,my_id ):
#   print(my_id)
#   return render(request,'enroll/show.html',{'id':my_id})

def showDetail(request,year ):
  student={'yr':year}
  return render(request,'enroll/show.html',student)



  
