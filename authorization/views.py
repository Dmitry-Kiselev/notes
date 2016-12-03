import json

from django.contrib.auth import login, authenticate
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
                    login(request, new_user)
                    return Response({'notes': reverse('note:notes_list', request=request, format=format)})
                else:
                    return Response({'has_error': True, 'errors': registration_form.error_messages})
            else:
                login_form = LoginForm(data=data)
                if login_form.is_valid():
                    login(request, login_form.get_user())
                    return Response({'notes': reverse('note:notes_list', request=request, format=format)})
                else:
                    return Response({'has_error': True, 'errors': login_form.error_messages})

        obj = {
            'login_form': login_form if login_form else LoginForm(),
            'registration_form': registration_form if registration_form else RegistrationForm(),
        }
        return render(request, 'authorization/authForm.html', obj)
    else:
        return Response({'notes': reverse('note:notes_list', request=request, format=format)})
