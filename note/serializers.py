from rest_framework import serializers

from .models import Note, Label, Category


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Note
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Label
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Category
        fields = ('name',)
