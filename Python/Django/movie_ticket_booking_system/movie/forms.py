# forms.py
from django import forms
from .models import User,Theaters
from django.contrib.auth.forms import AuthenticationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 
                'phone', 'address', 'city', 'state', 'country']
        
class TheaterForm(forms.ModelForm):
    class Meta:
        model = Theaters
        fields = '__all__' 
        
class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
