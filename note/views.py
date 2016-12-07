from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Note
from .permissions import IsOwnerOrDenial
from .serializers import NoteSerializer


class NoteList(ListCreateAPIView):
    """
    List all notes, or create a new note.
    """

    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a note instance.
    """
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user.pk)
