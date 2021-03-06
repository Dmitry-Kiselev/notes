from itertools import chain

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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
        """
        get notes which user owned or shared with current user
        """
        notes = Note.objects.filter(owner=self.request.user.pk)
        shared_with_user = Note.objects.filter(shared_with=self.request.user.pk)
        all_notes = chain(notes, shared_with_user)  # concatenating the querysets
        return all_notes

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
        try:
            parent_id = self.request.data['parent']['id']
            parent = Category.objects.get(pk=parent_id)
        except Exception:
            parent = None
        serializer.save(owner=self.request.user, parent=parent)


class CategoryDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a label instance.
    """
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user.pk)


def index(request):
    if request.user.is_authenticated:
        return render(request, 'note/index.html')
    else:
        return HttpResponseRedirect(reverse('auth'))


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


class ImageDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a image instance.
    """
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user.pk)


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


class FileDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a label instance.
    """
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user.pk)


class ListUsers(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [{'id': user.pk, 'name': user.username} for user in User.objects.all().exclude(pk=self.request.user.pk)]
        return Response(usernames)

    def put(self, request, format=None):
        """
        to delegate note to another user
        """
        note = Note.objects.get(pk=self.request.data.get('note'))
        user = self.request.data.get('user')
        note.shared_with.add(User.objects.get(username=user))
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        """
        to delete delegation relation
        """
        note = Note.objects.get(pk=self.request.query_params['note'])
        user = self.request.query_params['user']
        note.shared_with.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
