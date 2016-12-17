from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin

from .models import Note, Label, Category, Labelling, Categorization
from .permissions import IsOwnerOrDenial
from .serializers import NoteSerializer, LabelSerializer, LabellingSerializer, CategorySerializer, \
    CategorizationSerializer
from django.shortcuts import render


class NoteList(ListCreateAPIView):
    """
    List all notes, or create a new note.
    """

    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        note = Note.objects.get(text=self.request.data['text'])
        for l in self.request.data.get('labels'):
            label = Label.objects.get(pk=l)
            labelling = Labelling(note=note, label=label)
            labelling.save()


class NoteDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a note instance.
    """
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user.pk)

    def perform_update(self, serializer):
        note = Note.objects.get(pk=self.kwargs['pk'])
        old = Labelling.objects.filter(note=note)  # we sending entire note array every time
        # and if user deletes note we need be sure that it's will be deleted from database
        old.delete()
        for l in self.request.data['labels']:
            label = Label.objects.get(pk=l)
            labelling = Labelling(note=note, label=label)
            labelling.save()


class LabelList(ListCreateAPIView):
    """
    List all labels, or create a new label.
    """

    serializer_class = LabelSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LabelDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a label instance.
    """
    serializer_class = LabelSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user.pk)


class CategoryList(ListCreateAPIView):
    """
    List all labels, or create a new label.
    """

    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a label instance.
    """
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user.pk)


def index(request):
    return render(request, 'note/index.html')


"""
class LabelsRelations(CreateModelMixin, DestroyModelMixin):
    serializer_class = Labelling
    def get_queryset(self):
        return Labelling.objects.filter(note=)
    """
