from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from .models import Comment

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'image']
        widgets = {
            "body": Textarea(attrs={"cols": 75, "rows": 10}),
        }