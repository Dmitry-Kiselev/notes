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
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^notes/$', views.NoteList.as_view(), name='notes_list'),
    url(r'^notes/(?P<pk>[0-9]+)$', views.NoteDetails.as_view(), name='note_detail'),
    url(r'^labels/', views.LabelList.as_view(), name='labels_list'),
    url(r'^labels/(?P<pk>[0-9]+)$', views.LabelDetails.as_view(), name='label_detail'),
    url(r'^categories/', views.CategoryList.as_view(), name='categories_list'),
    url(r'^categories/(?P<pk>[0-9]+)$', views.CategoryDetails.as_view(), name='category_detail'),
    url(r'^$', views.index),
]

urlpatterns = format_suffix_patterns(urlpatterns)