from django import forms 
from django.core import validators

class StudentRegistration(forms.Form):    
  name=forms.CharField()
  password=forms.CharField(widget=forms.PasswordInput)
  rpassword=forms.CharField(widget=forms.PasswordInput)
  
  def clean(self):
    cleaned_data=super().clean()
    val_password=self.cleaned_data['password']
    val_rpassword=self.cleaned_data['rpassword']
    
    if val_password!=val_rpassword:
      raise forms.ValidationError("password is not match")
    
  
    
  
 