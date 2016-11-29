from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import RegistrationForm, LoginForm
import json
from django.contrib.auth import login, authenticate


def auth(request):
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
                return JsonResponse({'response': 'Now you can log in'})
            else:
                return JsonResponse({'has_error': True, 'errors': registration_form.error_messages})
        else:
            login_form = LoginForm(data=data)
            if login_form.is_valid():
                login(request, login_form.get_user())
                return JsonResponse({'response': 'You are logged in'})
            else:
                return JsonResponse({'has_error': True, 'errors': login_form.error_messages})

    obj = {
        'login_form': login_form if login_form else LoginForm(),
        'registration_form': registration_form if registration_form else RegistrationForm(),
    }
    return render(request, 'authorization/authForm.html', obj)
