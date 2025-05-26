from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwnerOrReadOnlyPublished


class UserNotesList(generics.ListAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class PublishedNotesList(generics.ListAPIView):
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



