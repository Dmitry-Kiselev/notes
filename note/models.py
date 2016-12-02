from django.db import models
from django.contrib.auth.models import User

colors = (
    ('Red', 'red'),
    ('Purple', 'purple'),
    ('Cyan', 'cyan'),
    ('Amber', 'amber'),
    ('Grey', 'grey'),
    ('Indigo', 'indigo'),
    ('Light green', 'light_green'),
    ('White', 'white')
)


class Note(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    attachment = models.FileField()
    color = models.CharField(choices=colors)


class Label(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    parent = models.ForeignKey('self')
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class File(models.Model):
    file = models.FileField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Delegation(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    delegate_to = models.ForeignKey(User, on_delete=models.CASCADE)


class Categorization(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Labelling(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)


class Gallery(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class FileStorage(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    file = models.ForeignKey(Image, on_delete=models.CASCADE)
