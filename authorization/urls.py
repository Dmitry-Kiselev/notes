"""notes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout

from .views import auth, ResetPasswordRequestView, PasswordResetConfirmView

urlpatterns = [
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^reset_password',
        ResetPasswordRequestView.as_view(), name="password_reset"),
    url(r'^password_reset/done/$',
        auth_views.password_reset_done, {'template_name': 'authorization/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'authorization/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'logout', logout, {"next_page": "/"}, name='logout'),
    url(r'$', auth, name='auth'),
]
