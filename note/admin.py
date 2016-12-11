from django.contrib import admin

from .models import Note, Label, Category, Categorization, Labelling

# Register your models here.
admin.site.register(Note)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(Labelling)
admin.site.register(Categorization)
