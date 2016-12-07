from rest_framework import serializers

from .models import Note, Label


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Note
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Label
        fields = ('name',)
