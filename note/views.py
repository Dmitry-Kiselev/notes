from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note, Label, Category, Image, File
from .permissions import IsOwnerOrDenial
from .serializers import NoteSerializer, LabelSerializer, CategorySerializer, \
    ImageSerializer, FileSerializer


class NoteList(ListCreateAPIView):
    """
    List all notes, or create a new note.
    """

    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user.pk) | Note.objects.filter(shared_with=self.request.user.pk)

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


class ImageList(ListCreateAPIView):
    """
    List all images, or create a new one.
    """
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FileList(ListCreateAPIView):
    """
    List all files, or create a new one.
    """
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListUsers(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

    def put(self, request, format=None):
        note = Note.objects.get(pk=self.request.data.get('note'))
        user = self.request.data.get('user')
        note.shared_with.add(User.objects.get(username=user))
        return Response(status=status.HTTP_201_CREATED)
