import json

from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from note.models import Label, Category
from notes.settings import DEFAULT_FROM_EMAIL
from .forms import PasswordResetRequestForm, SetPasswordForm
from .forms import RegistrationForm, LoginForm


@api_view(['GET', 'POST'])
def auth(request, format=None):
    if not request.user.is_authenticated:
        login_form, registration_form = False, False
        if request.method == "POST":
            data = json.loads(request.body.decode("utf-8"))
            if data.get('email'):  # some condition to distinguish between login and registration form
                registration_form = RegistrationForm(data)
                if registration_form.is_valid():
                    registration_form.save()
                    new_user = authenticate(username=data['username'],
                                            password=data['password1'],
                                            )
                    Label(name='Personal', owner=new_user).save()  # Create default labels and categories for new user.
                    #  Items created this way can be easily deleted by the user
                    Label(name='Work', owner=new_user).save()
                    Category(name='Important', owner=new_user).save()
                    Category(name='Funny', owner=new_user).save()
                    login(request, new_user)
                    return Response(status=status.HTTP_200_OK)
                else:
                    errors = []
                    for err_dict in registration_form.errors:
                        try:
                            for err in registration_form.errors[err_dict]:
                                errors.append(err)
                        except Exception as e:
                            Response({'has_error': True, 'errors': e})
                    return Response({'has_error': True, 'errors': errors})
            else:
                login_form = LoginForm(data=data)
                if login_form.is_valid():
                    login(request, login_form.get_user())
                    return Response({'notes': reverse('note:notes_list', request=request, format=format)})
                else:
                    errors = []
                    for err_dict in login_form.errors:
                        try:
                            for err in login_form.errors[err_dict]:
                                errors.append(err)
                        except Exception as e:
                            Response({'has_error': True, 'errors': e})
                    return Response({'has_error': True, 'errors': errors})

        obj = {
            'login_form': login_form if login_form else LoginForm(),
            'registration_form': registration_form if registration_form else RegistrationForm(),
        }
        return render(request, 'authorization/authForm.html', obj)
    else:
        return HttpResponseRedirect('/')


class ResetPasswordRequestView(FormView):
    """
    password reset views are based on https://github.com/ruddra/django-reset-password,
    but was highly simplified
    """
    success_url = '/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def reset_password(self, user, request):
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'your site',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        subject_template_name = 'authorization/password_reset_subject.txt'

        email_template_name = 'authorization/password_reset_email.html'

        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, DEFAULT_FROM_EMAIL,
                  [user.email], fail_silently=False)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data["email"]
            # uses the method written above
            if self.validate_email_address(data) is True:
                '''
                If the input is an valid email address, then the following code will lookup for users associated
                with that email address.
                '''
                associated_users = User.objects.filter(email=data)
                if associated_users.exists():
                    for user in associated_users:
                        self.reset_password(user, request)

                    result = self.form_valid(form)
                    return result
                result = self.form_invalid(form)
                return result
        except Exception:
            pass
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    success_url = '/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        user_model = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = user_model._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)
