from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Note
from .permissions import IsOwnerOrDenial
from .serializers import NoteSerializer


class NoteList(ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """

    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(pk=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDetails(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrDenial,)

    def get_queryset(self):
        return Note.objects.filter(pk=self.request.user.pk)
