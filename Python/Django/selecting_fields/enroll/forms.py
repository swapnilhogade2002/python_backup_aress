from django import forms
from .models import User

class UserRegistration(forms.ModelForm):
    class Meta:
        model = User 
        #option:01
        # fields = ("name","email","password")
        
        #option:02
        # fields = '__all__'
        
        #option: 03
        exclude=['name']

  