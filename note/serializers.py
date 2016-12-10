from rest_framework import serializers

from .models import Note, Label, Category, Labelling, Categorization


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    labels = serializers.ReadOnlyField(source='get_labels')
    categories = serializers.ReadOnlyField(source='get_categories')

    class Meta:
        model = Note
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Label
        fields = ('name', 'owner')


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Category
        fields = ('name', 'owner')


class LabellingSerializer(serializers.ModelSerializer):
    note = serializers.ReadOnlyField(source='note.id')
    label = serializers.ReadOnlyField(source='label.id')

    class Meta:
        model = Labelling
        fields = '__all__'


class CategorizationSerializer(serializers.ModelSerializer):
    note = serializers.ReadOnlyField(source='note.id')
    category = serializers.ReadOnlyField(source='category.id')

    class Meta:
        model = Categorization
        fields = '__all__'
