from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Note
from .serializers import NoteSerializer


class NoteList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request):
        notes = Note.objects.filter(pk=request.user.pk)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
