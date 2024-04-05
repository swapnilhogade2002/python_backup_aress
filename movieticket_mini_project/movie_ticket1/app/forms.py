from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth import authenticate
from.models import Customer, TheaterTicketBooking,Movies

ROLL_CHOICES = [
    ('user', 'User'),
    ('theater', 'Theater'),
]

class CustomerRegistrationForms(UserCreationForm):
  password1=forms.CharField(label='Password', 
                            widget=forms.PasswordInput(attrs={'class':'form-control'}))
  password2=forms.CharField(label='Confirm Password (again)', 
                            widget=forms.PasswordInput(attrs={'class':'form-control'}))
  email=forms.CharField(required= True,widget=forms.EmailInput(attrs={'class':'form-control'}))
  roll = forms.ChoiceField(choices=ROLL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
  class Meta:
    model=User 
    fields=['username','email','password1','password2','roll']
    labels={'email':'Email'}
    widgets={'username': forms.TextInput(attrs={
      'class':'form-control'
    })}
  
class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={
      'autofocus':True, 'class':'form-control'
    }))
    password=forms.CharField(label=_("Password"),strip=False, widget=forms.PasswordInput(attrs={
      'autocomplete':'current-password', 'class':'form-control'
    }))
# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(email=username)
#         except User.DoesNotExist:
#             return None
#         if user.check_password(password):
#             return user
#         return None

# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={
#         'autofocus': True, 'class': 'form-control'
#     }))
#     password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={
#         'autocomplete': 'current-password', 'class': 'form-control'
#     }))

#     def clean(self):
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')

#         if email and password:
#             self.user_cache = authenticate(self.request, username=email, password=password)
#             if self.user_cache is None:
#                 raise forms.ValidationError(
#                     self.error_messages['invalid_login'],
#                     code='invalid_login',
#                     params={'email': self.username_field.verbose_name},
#                 )
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         return self.cleaned_data



    

class MyPasswordChangeForm(PasswordChangeForm):
  old_password=forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput({
      'autocomplete':'new-password','autofocus':True ,'class':'form-control'
    }))
  new_password1=forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput({
      'autocomplete':'new-password','autofocus':True ,'class':'form-control'
    }),help_text=password_validation.password_validators_help_text_html())
  new_password2=forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput({
      'autocomplete':'new-password','autofocus':True ,'class':'form-control'
    }))

class MyPasswordResetForm(PasswordResetForm):
  email=forms.EmailField(label=_("Email"),max_length=201,
                         widget=forms.EmailInput(attrs={'autocomplete':'email'
                                                        ,'class':'form-control'}))
class MysetPasswordForm(SetPasswordForm):
  new_password1=forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput({
      'autocomplete':'new-password' ,'class':'form-control'
    }),help_text=password_validation.password_validators_help_text_html())
  new_password2=forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput({
      'autocomplete':'new-password','class':'form-control'
    }))

class CustomerProfileForm(forms.ModelForm):
  class Meta:
    model=Customer
    fields=['name','locality','city','state','zipcode']
    widgets={
      'name':forms.TextInput(attrs={'class':'form-control'}),
      'locality':forms.TextInput(attrs={'class':'form-control'}),
      'city':forms.TextInput(attrs={'class':'form-control'}),
      'state':forms.Select(attrs={'class':'form-control'}),
      'zipcode':forms.TextInput(attrs={'class':'form-control'}),
    }
    
# theater dashboard
class MoviesForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['titlee', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image', 'theater_name', 'show_time', 'address']
        widgets = {
            'titlee': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'theater_name': forms.TextInput(attrs={'class': 'form-control'}),
            'show_time': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
 
  
  
    