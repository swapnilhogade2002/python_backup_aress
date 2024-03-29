from django import forms 
from django.core import validators

# custom validation
def name_starts_with_s(value):
  if value[0]!='s':
    raise forms.ValidationError('name start with s')

class StudentRegistration(forms.Form):    
  
  #in built validation      
  # name= forms.CharField(validators=[validators.MaxLengthValidator(10)])
  # email=forms.EmailField()
  
  # custom validation
  name=forms.CharField(validators=[name_starts_with_s])
  
 