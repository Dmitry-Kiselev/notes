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
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    attachment = models.FileField(blank=True, null=True, upload_to='files/')
    color = models.CharField(choices=colors, max_length=20, default='grey')

    def __str__(self):
        return self.text[:10]

    @property
    def get_labels(self):
        return Labelling.objects.filter(note=self.pk).values_list('label', flat=True)

    @property
    def get_categories(self):
        return Categorization.objects.filter(note=self.pk).values_list('category', flat=True)


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
