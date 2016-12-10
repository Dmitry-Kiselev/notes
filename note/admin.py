from django.contrib import admin
from .models import Note, Label, Category


# Register your models here.
admin.site.register(Note)
admin.site.register(Label)
admin.site.register(Category)