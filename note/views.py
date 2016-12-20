from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Note, Label, Category, Image, File
from .permissions import IsOwnerOrDenial
from .serializers import NoteSerializer, LabelSerializer, CategorySerializer, \
    ImageSerializer
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


class NoteDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a note instance.
    """
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user.pk)


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
