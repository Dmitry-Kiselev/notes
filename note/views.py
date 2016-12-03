from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer


class NoteList(APIView):
    def get(self, request):
        notes = Note.objects.filter(pk=request.user.pk)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
