from django import forms 

class StudentRegistration(forms.Form):          
  name= forms.CharField()
  email=forms.EmailField()
  
  def clean(self):
    cleaned_data=super().clean()
    
    valname=cleaned_data.get('name')
    valemail=cleaned_data.get('email')
    
    if len(valname) <4:
      raise forms.ValidationError("Enter more than 4 char name")
    
    if len(valemail)<4:
      raise forms.ValidationError("Enter more than 4 charecter in email")
    
    
    # signle field validation
    
    # valname=self.cleaned_data['name']  
    # if len(valname)<4:
    #   raise forms.ValidationError("Enter charecter more than 4")
    # return valname
  