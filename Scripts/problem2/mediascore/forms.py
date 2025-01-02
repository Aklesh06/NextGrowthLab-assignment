from django import forms
from .models import AndroidApp, RegisterUser, ClientInfo

class RegisterForm(forms.ModelForm):
    class Meta:
        model = RegisterUser
        fields = ['email','username','password']
        
        password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})),
       
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),       
        }

class AndroidAppForm(forms.ModelForm):
    class Meta:
        model = AndroidApp
        fields = ['appName','appLink','icon','category','subCategory','points']
        widgets = {
            'appName': forms.TextInput(attrs={'id':'name','class': 'form-control', 'placeholder': 'Enter app name'}),
            'appLink': forms.URLInput(attrs={'id':'link','class': 'form-control', 'placeholder': 'Enter app link'}),
            'icon': forms.ClearableFileInput(attrs={'id':'image','class': 'form-data'}),
            'category': forms.Select(attrs={'id':'category','class': 'form-control'}),
            'subCategory': forms.Select(attrs={'id':'subcategory','class': 'form-control'}),
            'points': forms.NumberInput(attrs={'id':'points','class': 'form-point', 'placeholder': 'Enter points'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [('', 'Enter category')] + list(self.fields['category'].choices)
        self.fields['subCategory'].choices = [('', 'Enter sub-category')] + list(self.fields['subCategory'].choices)
        
