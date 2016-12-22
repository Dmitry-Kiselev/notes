from rest_framework import serializers

from .models import Note, Label, Category, Image, File


class LabelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Label
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    image = serializers.ImageField(max_length=None, use_url=True, )

    class Meta:
        model = Image
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    labels = LabelSerializer(many=True)
    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        labels = validated_data.pop('labels')
        images = self.initial_data.get('images')
        note = Note.objects.create(**validated_data)
        for label in labels:
            note.labels.add(Label.objects.get(name=label["name"]))
        if images:
            for img in images:
                image = Image.objects.get(pk=img['id'])
                note.images.add(image)
        return note

    def update(self, instance, validated_data):
        if instance:
            labels = validated_data.pop('labels')
            images = self.initial_data.get('images')
            instance.labels.clear()
            instance.images.clear()
            for label in labels:
                instance.labels.add(Label.objects.get(name=label["name"]))
            if images:
                for img in images:
                    image = Image.objects.get(pk=img['id'])
                    instance.images.add(image)
            return instance
