from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwner, IsOwnerOrReadOnlyPublished


class UserNotes(generics.ListAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class publishedNotes(generics.ListAPIView):
    queryset = Note.objects.filter(published=True)
    serializer_class = NoteSerializer


class NoteCreate(generics.CreateAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    
class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyPublished]


class NotePublish(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        
        if note.published:
            return Response(
                 {"detail": "This note is already published"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        note.published = True
        note.save()
        serializer = NoteSerializer(instance=note)
        return Response(serializer.data)
