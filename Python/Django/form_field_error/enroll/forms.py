from django import forms 
from django.core import validators

class StudentRegistration(forms.Form):    
  name=forms.CharField(error_messages={'required':'Enter password'})
  password=forms.CharField(error_messages={'required':'Enter your name'})
  rpassword=forms.CharField(error_messages={'required':'Enter password'})
  
 
    
  
    
  
 