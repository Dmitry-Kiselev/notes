from django.contrib.auth.models import User
from django.db import models

colors = (
    ('red darken-1', 'red'),
    ('purple darken-1', 'purple'),
    ('cyan darken-1', 'cyan'),
    ('amber accent-1', 'amber'),
    ('blue-grey darken-1', 'grey'),
    ('indigo darken-1', 'indigo'),
    ('light-green darken-1', 'light green'),
    ('pink darken-1', 'pink')
)


class Note(models.Model):
    title = models.CharField(max_length=120, null=True, blank=True)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    color = models.CharField(choices=colors, max_length=20, default='blue-grey darken-1')
    labels = models.ManyToManyField('Label', blank=True)
    categories = models.ManyToManyField('Category', blank=True)
    images = models.ManyToManyField('Image', blank=True)
    files = models.ManyToManyField('File', blank=True)
    shared_with = models.ManyToManyField(User, related_name='collaborators', blank=True)

    def __str__(self):
        return self.text[:10]


class Label(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class File(models.Model):
    file = models.FileField(upload_to='files/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
