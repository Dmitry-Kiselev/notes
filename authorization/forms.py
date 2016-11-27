from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'ng-model': 'userdata.username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'ng-model': 'userdata.email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'ng-model': 'userdata.password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'ng-model': 'userdata.password2'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'ng-model': 'userdata.username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'ng-model': 'userdata.password'}))
