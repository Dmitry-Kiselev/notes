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


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2
