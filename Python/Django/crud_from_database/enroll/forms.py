from django import forms 
from django.core import validators

class StudentRegistration(forms.Form):    
  name=forms.CharField(error_messages={'required':'Enter password'})
  email=forms.EmailField(error_messages={'required':'enter email'})
  password=forms.CharField(error_messages={'required':'Enter your name'})
 
  
 
    
  
    
  
 