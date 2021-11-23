from django import forms
from .models import UserModel

class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=6,widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserModel
        fields = ('username','email','phone','user_type','password')
    
    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('confirm_password')

        if pass1 != pass2:
            raise forms.ValidationError('Passwords do not match')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(min_length=6,widget=forms.PasswordInput)