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


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    file = serializers.FileField(max_length=None, use_url=True, )

    class Meta:
        model = File
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    labels = LabelSerializer(many=True)
    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        labels = validated_data.pop('labels')
        images = self.initial_data.get('images')
        files = self.initial_data.get('files')
        note = Note.objects.create(**validated_data)
        for label in labels:
            note.labels.add(Label.objects.get(name=label["name"]))
        if images:
            for img in images:
                image = Image.objects.get(pk=img['id'])
                note.images.add(image)
        if files:
            for f in files:
                file = File.objects.get(pk=f['id'])
                note.images.add(file)
        return note

    def update(self, instance, validated_data):
        if instance:
            labels = validated_data.pop('labels')
            images = self.initial_data.get('images')
            files = self.initial_data.get('files')
            instance.labels.clear()
            instance.images.clear()
            instance.files.clear()
            for label in labels:
                instance.labels.add(Label.objects.get(name=label["name"]))
            if images:
                for img in images:
                    image = Image.objects.get(pk=img['id'])
                    instance.images.add(image)
            if files:
                for f in files:
                    file = File.objects.get(pk=f['id'])
                    instance.files.add(file)
            return instance
