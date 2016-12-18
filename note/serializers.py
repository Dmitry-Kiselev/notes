from rest_framework import serializers

from .models import Note, Label, Category, Labelling, Categorization, Image, File


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    labels = serializers.ReadOnlyField(source='get_labels')
    categories = serializers.ReadOnlyField(source='get_categories')

    class Meta:
        model = Note
        fields = ('id', 'text', 'owner', 'image', 'attachment', 'color', 'labels', 'categories')


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


class ImageSerializer(serializers.ModelSerializer):
    note = serializers.ReadOnlyField(source='note.id')
    image = Base64ImageField(max_length=None, use_url=True, )

    class Meta:
        model = Image
        fields = '__all__'
