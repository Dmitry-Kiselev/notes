from rest_framework import serializers

from .models import Note, Label, Category, Image, File


class LabelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # to make id field accessible in validated_data
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Label
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # to make id field accessible in validated_data
    owner = serializers.ReadOnlyField(source='owner.id')
    parent = serializers.ReadOnlyField(required=False, source='parent.id')

    class Meta:
        model = Category
        fields = ('id', 'name', 'owner', 'parent',)


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
    labels = LabelSerializer(many=True, required=False)
    categories = CategorySerializer(many=True, required=False)
    images = ImageSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'owner', 'text', 'labels', 'categories', 'images', 'files', 'color', 'shared_with', 'title')

    def create(self, validated_data):

        labels = validated_data.pop('labels') if 'labels' in validated_data else None
        categories = validated_data.pop('categories') if 'categories' in validated_data else None  # we have to use pop
        # to make sure what categories won't be in validated_data, because note's method save() must to be called
        # before adding ManyToMany relations. Same for labels.
        images = self.initial_data.get('images')
        files = self.initial_data.get('files')

        note = Note.objects.create(**validated_data)
        if labels:
            for label in labels:
                note.labels.add(Label.objects.get(id=label["id"]))
        if images:
            for img in images:
                image = Image.objects.get(pk=img['id'])
                note.images.add(image)
        if files:
            for f in files:
                file = File.objects.get(pk=f['id'])
                note.files.add(file)
        if categories:
            for c in categories:
                category = Category.objects.get(pk=c['id'])
                note.categories.add(category)
        return note

    def update(self, instance, validated_data):
        if instance:
            labels = validated_data.pop('labels')
            images = self.initial_data.get('images')
            files = self.initial_data.get('files')
            categories = validated_data.pop('categories')
            instance.color = validated_data.pop('color')
            instance.title = validated_data.pop('title')
            instance.text = validated_data.pop('text')
            old_images = [x for x in instance.images.all()]
            old_files = [x for x in instance.files.all()]
            # delete all ManyToMany relations and recreate them if they still exists, and add new one
            instance.labels.clear()
            instance.images.clear()
            instance.files.clear()
            for label in labels:
                instance.labels.add(Label.objects.get(pk=label["id"]))
            if images:
                for img in images:
                    image = Image.objects.get(pk=img['id'])
                    instance.images.add(image)
            if files:
                for f in files:
                    file = File.objects.get(pk=f['id'])
                    instance.files.add(file)
            if categories:
                for c in categories:
                    category = Category.objects.get(pk=c['id'])
                    instance.categories.add(category)
            instance.save()
            for i in old_images:
                if i not in instance.images.all():
                    img = Image.objects.get(pk=i.pk)
                    img.delete()
            for f in old_files:
                if f not in instance.files.all():
                    file = File.objects.get(pk=f.pk)
                    file.delete()
            return instance
