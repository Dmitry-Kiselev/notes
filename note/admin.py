from django.contrib import admin

from .models import Note, Label, Category, Image, File

# Register your models here.
admin.site.register(Note)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(File)
