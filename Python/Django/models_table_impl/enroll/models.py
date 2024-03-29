from django.db import models

# Create your models here.

class Student(models.Model):
  studid=models.IntegerField()
  stuname=models.CharField(max_length=20)
  stuemail=models.EmailField()
  
  
